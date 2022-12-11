import os

from flask import Flask, render_template, redirect, flash, request, abort, session
# For auth:
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from utilities import is_safe_url
from models import db, connect_db, User
from forms import RegistrationForm, LoginForm, ApiJobSearchForm, UserEditForm
from api_requests import get_jobs, get_job_details

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

@app.route('/jobs')
def jobs_page():
    """Shows form to search jobs through Career OneStop API"""

    form = ApiJobSearchForm()

    return render_template('job_search.html', form=form)

@app.route('/jobs/search')
def jobs_search_result():
    """Shows the results of a job search through Career OneStop API"""

    form = ApiJobSearchForm(request.args, meta={'csrf': False})
    if form.validate():
        results_dict = get_jobs(form)
        first_job_details = get_job_details(results_dict['Jobs'][0]['JvId'])

    return render_template('job_search_results.html', form=form, results=results_dict, details=first_job_details)

@app.route('/jobs/details/<job_id>/json')
def send_job_details_json(job_id):
    """Sends json of job details to be handled by JavaScript"""

    results_json = get_job_details(job_id)
    return results_json