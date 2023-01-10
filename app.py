import os

from flask import Flask, render_template, redirect, flash, request, abort, make_response, jsonify, session
# For auth:
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from markupsafe import Markup

from utilities import is_safe_url
from models import db, connect_db, User, SavedJob, JobHunt, JobApp, Factor
from forms import RegistrationForm, LoginForm, ApiJobSearchForm, ManualJobAddForm, NewJobHuntForm, SavedJobRegularEditForm, SavedJobCosEditForm, UserEditForm
from api_requests import get_jobs, get_job_details, get_page_navigation_values, get_postings_for_dashboard

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///jobalyze'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "aji32ojfuJHwp")

connect_db(app)

# with app.app_context():
#     db.drop_all()
#     db.create_all()

# For auth:
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in to acccess this page."
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Home:

@app.route('/')
def homepage():
    """Show homepage"""

    if current_user.is_anonymous:
        form = LoginForm()
        return render_template('home_anon.html', form=form, current_user=current_user)
    else:
        return render_template('home_user.html', current_user=current_user)

# Authorization:

@app.route('/register', methods=["GET", "POST"])
def register():
    """Register User"""

    if current_user.is_authenticated:
        flash(f'{current_user.username} is already logged in.')
        return redirect('/')

    form = RegistrationForm()

    if form.validate_on_submit():
        new_user = User.signup(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data
            )
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as err:
            if err.code == 'gkpj':
                form.username.errors.append(f"{err.params['username']} already exists.")
            else:
                form.username.errors.append('Registration failed. Please try again later.')
            return render_template('register.html', form = form, current_user=current_user)

        # login user
        login_user(new_user)
        flash(f'Welcome {new_user.username}!')

        return redirect('/')
    else:
        return render_template('register.html', form = form, current_user=current_user)

@app.route('/login', methods=["GET", "POST"])
def login():
    "Show login form and handle submission"

    if current_user.is_authenticated:
        flash(f'{current_user.username} is already logged in.')
        return redirect('/')

    form = LoginForm()
    if form.validate_on_submit():
        authenticated_user = User.authenticate_user(
            username = form.username.data,
            password = form.password.data
        )
        if authenticated_user:
            login_user(authenticated_user)
            flash(f'Welcome {authenticated_user.username}!')

            next = request.args.get('next')
            # is_safe_url should check if the url is safe for redirects.
            if not is_safe_url(next, request.host_url):
                return abort(400)

            return redirect(next or '/')
        else:
            form.password.errors = ['Incorrect username or password.']
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """Logs out a user"""

    logout_user()
    return redirect('/')

@app.route('/cos-jobs')
def jobs_page():
    """Shows form to search jobs through Career OneStop API"""

    form = ApiJobSearchForm()

    return render_template('job_search.html', form=form)

@app.route('/cos-jobs/search')
def jobs_search_result():
    """Shows the results of a job search through Career OneStop API"""

    form = ApiJobSearchForm(request.args, meta={'csrf': False})
    if form.validate():
        results_dict = get_jobs(form)
        if results_dict.get('ErrorCode'):
            return render_template('api_error.html', results_dict=results_dict)
        page_data = get_page_navigation_values(form)

    return render_template('job_search_results.html', form=form, results=results_dict, page_data=page_data)

@app.route('/cos-jobs/details/<cos_id>/json')
def send_job_details_json(cos_id):
    """Sends json of job details to be handled by JavaScript"""

    results_json = get_job_details(cos_id)
    # Check to see if job is already saved:
    if current_user.is_authenticated:
        if SavedJob.already_saved(current_user.id, cos_id):
            print('****Already Saved*****')
            results_json['saved'] = 'true'

    return results_json

@app.route('/cos-jobs/details/<cos_id>', methods=["GET", "POST"])
def show_job_details_page(cos_id):
    """Shows a job details page for an api job"""

    # Create "mock" saved job object to avoid errors on popup-ja.html render since real saved job object
        # is used in '/saved-jobs/<saved_job_id>' (which also uses poup-ja.html) and in which saved job
        # object values are used to populate parts of popup-ja.html.
    # In this view function, 'id' in some cases will be filled when job is already saved.
    # 'id' is used to decide whether to display saved icon and to avoid backend call in iAppliedButtonClick() in job_details_api.js.
    # 'id' (sometimes), 'title', and 'company' will be populated by job_details_api.js.

    saved_job = {'id': None, 'title': None, 'company': None}
    applied = False

    # Check to see if job is already saved:
    if current_user.is_authenticated:
        saved_job['id'] = SavedJob.already_saved_id(current_user.id, cos_id)
        if saved_job['id'] is not None:
            applied = JobApp.check_if_applied(saved_job['id'])
        active_hunts = JobHunt.get_active_job_hunts(current_user.id)
        if not active_hunts:
            form = NewJobHuntForm()
            if form.validate_on_submit():
                new_hunt = JobHunt.save_job_hunt(current_user.id, form.data)
                # ******************** Add failed API error handling ******************
                active_hunts.append(new_hunt)
                popup_ja = 'open'
                popup_jh = None
            else:
                popup_ja = None
                popup_jh = 'ready'
        else:
            form = None
            popup_ja = 'ready'
            popup_jh = None
    else:
        form = None
        active_hunts = None
        popup_ja = None
        popup_jh = None

    # Job details API request are sent from front end after page loads

    return render_template('job_details_api.html',
                            cos_id=cos_id,
                            fc=request.args['fc'],
                            saved_job=saved_job,
                            form=form,
                            active_hunts=active_hunts,
                            popup_ja=popup_ja,
                            popup_jh=popup_jh,
                            applied=applied)  

@app.route('/saved-jobs/add/cos', methods=['POST'])
@login_required
def save_job():
    """Saves a job to the database"""

    saved_job_id = SavedJob.save_job(current_user.id, request.get_json())

    # *******************return proper response object**********************
    return str(saved_job_id)

@app.route('/saved-jobs/add', methods=['Get', 'POST'])
@login_required
def add_job():
    """Allows user to add a manually entered job to saved jobs through a form"""

    form = ManualJobAddForm()

    if form.validate_on_submit():
        saved_job_id = SavedJob.save_job(current_user.id, form.data)
        # ******************** Add failed API error handling ******************
        return redirect(f'/saved-jobs/{saved_job_id}')

    return render_template('job_add.html', form=form)

@app.route('/saved-jobs/<saved_job_id>', methods=["GET", "POST"])
@login_required
def show_saved_job(saved_job_id):
    """Shows details of a particular saved job"""

    applied = JobApp.check_if_applied(saved_job_id)
    active_hunts = JobHunt.get_active_job_hunts(current_user.id)
    if not active_hunts:
        form = NewJobHuntForm()
        if form.validate_on_submit():
            new_hunt = JobHunt.save_job_hunt(current_user.id, form.data)
            # ******************** Add failed API error handling ******************
            active_hunts.append(new_hunt)
            popup_ja = 'open'
            popup_jh = None
        else:
            popup_ja = None
            popup_jh = 'ready'
    else:
        form = None
        popup_ja = 'ready'
        popup_jh = None
    saved_job_raw = SavedJob.query.get(saved_job_id)
    saved_job = SavedJob.translate_values(saved_job_raw)
    description = Markup(saved_job.job_description)

    return render_template('job_details_saved.html',
                            saved_job=saved_job,
                            description=description,
                            form=form,
                            active_hunts=active_hunts,
                            popup_ja=popup_ja,
                            popup_jh=popup_jh,
                            applied=applied)

@app.route('/saved-jobs/<saved_job_id>/edit', methods=["GET", "POST"])
@login_required
def edit_saved_job(saved_job_id):
    """Edits details of a particular saved job."""

    # saved_job values do not need to be translated since select fields need database value
    # This save_job object is equivalent to save_job_raw in '/saved-jobs/<saved_job_id>'
    saved_job = SavedJob.query.get(saved_job_id)
    if saved_job.cos_id:
        print('Yes COS ID')
        form = SavedJobCosEditForm()
    else:
        print('No COS ID')
        form = SavedJobRegularEditForm()

    if form.validate_on_submit():
        saved_job_id = SavedJob.save_job(current_user.id, form.data)

    description = Markup(saved_job.job_description)

    return render_template('saved-job-edit.html',
                            saved_job=saved_job,
                            description=description,
                            form=form)

@app.route('/saved-jobs/<saved_job_id>/edit/json', methods=['POST'])
@login_required
def edit_saved_job_json(saved_job_id):
    """Endpoint for frontend to post an edit to a saved job. Used for the Add buttons on incomplete saved jobs."""

    resp = SavedJob.edit_saved_job(current_user.id, saved_job_id, request.get_json())

    # ********************** JS can't see the body of response **************************
    return make_response(resp['body']['message'], resp['status'])

@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard_page_no_hunt():
    """Shows generic dashboard page to user who has not created a hunt"""

    form = NewJobHuntForm()

    if form.validate_on_submit():
        print('Job Hunt form validated')
        new_hunt = JobHunt.save_job_hunt(current_user.id, form.data)
        # ******************** Add failed API error handling ******************
        return redirect('/dashboard')

    current_hunt = User.current_hunt(current_user)
    if current_hunt:
        return redirect(f'/dashboard/{current_hunt.id}')

    saved_jobs_list = SavedJob.get_dashboard_saved_jobs_list(current_user.id)

    return render_template('dashboard.html',
        current_hunt = current_hunt,
        saved_jobs_list = saved_jobs_list,
        job_apps_list = None,
        new_job_postings = None,
        goals = None,
        form = form)

@app.route('/dashboard/<hunt_id>', methods=['GET', 'POST'])
@login_required
def dashboard_page_load_hunt(hunt_id):
    """Shows dashboard page with information displayed pertaining to chosen hunt"""

    # job_hunts (retrieved in template from current_user object)
    # saved_jobs (available from current_user)
    # current job_hunt (queried below)
    # job_apps (available from current job_hunt)
    # recent job postings (get from front end)

    form = NewJobHuntForm()

    if form.validate_on_submit():
        print('Job Hunt form validated')
        new_hunt = JobHunt.save_job_hunt(current_user.id, form.data)
        # ******************** Add failed API error handling ******************
        return redirect('/dashboard')

    current_hunt = JobHunt.query.get(hunt_id)
    saved_jobs_list = SavedJob.get_dashboard_saved_jobs_list(current_user.id)
    job_apps_list = JobApp.get_dashboard_job_apps_list(current_user.id)
    new_job_postings = get_postings_for_dashboard(current_hunt)
    goals = None

    return render_template('dashboard.html',
        current_hunt=current_hunt,
        saved_jobs_list=saved_jobs_list,
        job_apps_list=job_apps_list,
        new_job_postings=new_job_postings,
        goals=goals,
        form=form)

@app.route('/job-hunts/add', methods=['POST'])
@login_required
def save_job_hunt():
    """Saves a job hunt to the database"""

    saved_job_hunt = JobHunt.save_job(current_user.id, request.get_json())

    # fix this return
    return "success"  

@app.route('/job-apps/add/json', methods=['POST'])
@login_required
def save_job_app():
    """Endpoint for frontend to add (report) a job app."""

    app_details = request.get_json()
    resp = JobApp.add_job_app(app_details)

    if resp['status'] == 200:
        factors_list = JobHunt.getFactors(app_details['job_hunt_id'])

        return factors_list

    # ********************** JS can't see the body of response **************************
    return make_response(resp['body']['message'], resp['status'])


@app.route('/factors/add/json', methods=['POST'])
@login_required
def save_factor():
    """Endpoint that Accepts a list of new factors to add to the database"""

    factors_to_add = request.get_json()
    resp = Factor.add_factors(factors_to_add, current_user.id)

    if resp['status'] == 200:
        return resp['body']

    # ********************** JS can't see the body of response **************************
    return make_response(resp['body']['message'], resp['status'])

@app.route('/factors/associate/json', methods=['POST'])
@login_required
def associate_factor():
    """Endpoint that Accepts a list of new factors' ids to associate them with a job app by adding to the app_factor table in the database."""

    associate_factors_dict = request.get_json()
    resp = Factor.associate_factors(associate_factors_dict, current_user.id)
    import pdb; pdb.set_trace()

    if resp['status'] == 200:
        return resp['body']

    # ********************** JS can't see the body of response **************************
    return make_response(resp['body'], resp['status'])