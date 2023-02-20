from datetime import datetime, date, timedelta

from flask import session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table
from flask_login import UserMixin

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)

# --------------------------- User -------------------------------------------------------------------------------------------------

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    email = db.Column(
        db.String(100),
        nullable=False,
        unique=True
    )
    username = db.Column(
        db.String(40),
        nullable=False,
        unique=True
    )
    password = db.Column(
        db.Text,
        nullable=False
    )
    first_name = db.Column(
        db.String(40)
    )
    last_name = db.Column(
        db.String(40)
    )
    country = db.Column(
        db.String(50)
    )
    state = db.Column(
        db.String(40)
    )
    linkedin_url = db.Column(
        db.String(150)
    )
    date_registered = db.Column(
        db.Date,
        nullable=False,
        default=date.today()
    )
    saved_jobs = db.relationship('SavedJob', back_populates='user', cascade="all, delete")
    job_apps = db.relationship('JobApp', back_populates='user')
    job_hunts = db.relationship('JobHunt', back_populates='user', cascade="all, delete")

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    def current_hunt(self):
        """Find a users most recent job hunt"""
        if self.job_hunts:
            return self.job_hunts[-1]
        return None

    def change_password(self, new_password):
        """Changes a user's password."""

        hashed_new_pwd = bcrypt.generate_password_hash(new_password).decode('UTF-8')

        self.password = hashed_new_pwd
        db.session.add(self)
        db.session.commit()

        return "success!"

    @classmethod
    def signup(cls, email, username, password):
        """Hashes user password and adds user to database.
        Returns new user SQLAlchemy object or error dict."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user_to_register = cls(
            email=email,
            username=username,
            password=hashed_pwd
        )

        db.session.add(user_to_register)
        try:
            db.session.commit()
        except Exception as err:
            if err.code == 'gkpj':
                return {'error': 409, 'message': f"{err.params['username']} already exists."}
            else:
                return {'error': 500, 'message': 'Registration failed. Please try again later.'}

        return user_to_register

    @classmethod
    def authenticate_user(cls, username, password):
        """Authenticates user on log in and returns user instance"""

        user = cls.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

# --------------------------- JobHunt -------------------------------------------------------------------------------------------------

class JobHunt(db.Model):

    __tablename__ = 'job_hunts'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(50),
        nullable=False
    )
    job_title_desired = db.Column(
        db.Text,
        nullable=False
    )
    o_net_code = db.Column(
        db.String(10)
    )
    location = db.Column(db.String(100),
        nullable=False,
        default='US')
    radius = db.Column(db.Integer,
        nullable=False,
        default=0)
    non_us = db.Column(db.Boolean,
        nullable=False,
        default=False)
    remote = db.Column(db.Boolean,
        nullable=False,
        default=False)
    date_begun = db.Column(
        db.Date,
        nullable=False,
        default=date.today()
    )
    hired_by_goal_date = db.Column(db.Date)
    app_goal_time_frame = db.Column(db.String(1))
    # values:
    #     d: Daily
    #     w: Weekly
    #     m: Monthly
    app_goal_number = db.Column(db.Integer)
    status = db.Column(
        db.String(1),
        default='a'
    )
    # values:
    #     a: Actively Applying
    #     p: On Pause
    #     h: Closed, Hired
    #     c: Closed, Abandoned
    
    description = db.Column(
        db.Text
    )
    date_closed = db.Column(
        db.Date
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable = False
    )
    hired_by_app_id = db.Column(db.Integer)
    # value referes to JobApp id
    # no postgres relationship used to avoid error
    
    user = db.relationship('User', back_populates='job_hunts')
    job_apps = db.relationship('JobApp', back_populates='job_hunt', cascade="all, delete")
    factors = db.relationship("Factor", back_populates="job_hunt", cascade="all, delete")

    def __repr__(self):
        return f"<Job Hunt #{self.id}: {self.job_title_desired}, {self.status}>"

    def translate_values(self):
        """Changes values from database abreviations to actual values for display."""

        if self.app_goal_time_frame:
            agtf_translator = {'d': 'Daily', 'w': 'Weekly', 'm': 'Monthly'}
            self.app_goal_time_frame_translated = agtf_translator[self.app_goal_time_frame]

        if self.status:
            status_translator = {'a': 'Actively Applying', 'p': 'On Pause', 'h': 'Closed, Hired', 'c': 'Closed, Abandoned'}
            self.status_translated = status_translator[self.status]

        return self

    def delete_job_hunt(self):
        """Deletes a job hunt."""

        db.session.delete(self)
        db.session.commit()

        return {'body': 'success!', 'status': 200}

    @classmethod
    def save_job_hunt(cls, user_id, hunt_obj):
        """Saves a job hunt."""

        hunt_to_save = cls(user_id = user_id)

        for key in hunt_obj:
            setattr(hunt_to_save, key, hunt_obj[key])

        # **********************need some error handling if not saved**********************
        db.session.add(hunt_to_save)
        db.session.commit()
        return hunt_to_save

    @classmethod
    def edit_job_hunt(cls, user_id, job_hunt_id, details_obj):
        """Edits a job hunt. Returns an object to be converted into a response object in app.py."""

        hunt_to_edit = cls.query.get(job_hunt_id)
        if hunt_to_edit.user_id == user_id:
            print ('************** User Ids matched! *******************')

            if details_obj.get('status') in ['h', 'c'] and hunt_to_edit.status in ['a', 'p']:
                details_obj['date_closed'] = date.today()

            details_obj = cls.coerce_non_us(details_obj)

            try:
                for key in details_obj:
                    setattr(hunt_to_edit, key, details_obj[key])
                db.session.add(hunt_to_edit)
                db.session.commit()
            except: 
                return {'body': {'message': 'Sorry, we were unable to process your request. Please try again later!'}, 'status': 500}
            return {'body': {'message': 'Update Successful!'}, 'status': 200}
        else:
            return {'body': {'message': 'Unauthorized: This saved job is associated with another user.'}, 'status': 403}

    @classmethod
    def coerce_non_us(cls, details_obj):
        """Changes 'False' and 'True' string values into true Booleans for non_us value."""

        if details_obj.get('non_us') == 'True':
            details_obj['non_us'] = True

        if details_obj.get('non_us') == 'False':
            details_obj['non_us'] = False

        return details_obj

    @classmethod
    def get_active_job_hunts(cls, user_id):
        """Returns a list of active job hunts for a user."""

        return db.session.query(cls).filter(cls.user_id == user_id, cls.status == 'a').order_by(cls.id.desc()).all()

    @classmethod
    def get_active_job_hunt_ids(cls, user_id):
        """Returns a list of active job hunts for a user."""

        return db.session.query(cls.id).filter(cls.user_id == user_id, cls.status == 'a').order_by(cls.id.desc()).all()

    @classmethod
    def get_job_hunt_by_id(cls, job_hunt_id, translate_values=False):

        job_hunt = JobHunt.query.get(job_hunt_id)

        if translate_values:
            job_hunt = job_hunt.translate_values()

        return job_hunt

    @classmethod
    def getFactors(cls, job_hunt_id):
        """Returns factors for a given job hunt id"""

        job_hunt = cls.query.get(job_hunt_id)
        factors_list = [{'id': x.id, 'name': x.name} for x in job_hunt.factors]

        return factors_list

# --------------------------- SavedJob -------------------------------------------------------------------------------------------------

class SavedJob(db.Model):

    __tablename__ = 'saved_jobs'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    company = db.Column(
        db.Text,
        nullable=False
    )
    title = db.Column(
        db.Text,
        nullable=False
    )
    date_saved = db.Column(
        db.Date,
        nullable=False,
        default=date.today()
    )
    date_posted = db.Column(
        db.Date
    )
    # date posted from api is in "%Y-%M-%d %I:%M %p" format

    location = db.Column(
        db.String(100)
    )
    company_size = db.Column(
        db.Integer
    )
    # range: 1-8
    # values:
    #     1: 1-10 employees.
    #     2: 11-50 employees.
    #     3: 51-200 employees.
    #     4: 201-500 employees.
    #     5: 501-1,000 employees.
    #     6: 1,001-5,000 employees.
    #     7: 5,001-10,000 employees.
    #     8: 10,001+ employees.

    job_type = db.Column(
        db.String(1)
    )
    # range: 1-5
    # values:
    #     f: Full-time
    #     p: Part-time
    #     c: Contract
    #     i: Internship
    #     v: Volunteer

    experience_level = db.Column(
        db.String(1)
    )
    # range: 1-6
    # values:
    #     i: Internship
    #     e: Entry level
    #     a: Associate
    #     m: Mid-Senior level
    #     d: Director
    #     x: Executive
    salary_min = db.Column(
        db.Integer
    )
    salary_max = db.Column(
        db.Integer
    )
    job_description = db.Column(
        db.Text
    )
    application_link = db.Column(
        db.Text
    )
    cos_id = db.Column(
        db.Text
    )
    federal_contractor = db.Column(
        db.Boolean
    )
    user_notes = db.Column(
        db.Text
    )
    last_cos_update = db.Column(db.Date,
        default=date.today())
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable = False
    )
    user = db.relationship('User', back_populates='saved_jobs')
    job_app = db.relationship("JobApp", back_populates="saved_job", uselist=False, cascade="all, delete")
    # Make sure to not allow or at least warn a user that deleting a saved job that has a job app
    # will also delete the job app.

    def __repr__(self):
        return f"<Job #{self.id}: {self.company}, {self.title}>"

    def translate_values(self):
        """Changes values from database abreviations to actual values for display."""

        if self.company_size:
            cs_translator = [None, '1-10 employees', '11-50 employees', '51-200 employees', '201-500 employees',
            '501-1,000 employees', '1,001-5,000 employees', '5,001-10,000 employees', '10,001+ employees']
            self.company_size_translated = cs_translator[self.company_size]

        # Salary range locale string translation done in job-details-saved.js

        if self.job_type:
            jt_translator = {'f': 'Full-time', 'p': 'Part-time', 'c': 'Contract', 'i': 'Internship', 'v': 'Volunteer'}
            self.job_type_translated = jt_translator[self.job_type]

        if self.federal_contractor != None:
            fc_translator = {True: 'Yes', False: 'No'}
            self.federal_contractor_translated = fc_translator[self.federal_contractor]

        if self.experience_level:
            el_translator = {'i': 'Internship', 'e': 'Entry level', 'a': 'Associate',
            'm': 'Mid-Senior level', 'd': 'Director', 'x': 'Executive'}
            self.experience_level_translated = el_translator[self.experience_level]

        return self

    @classmethod
    def save_job(cls, user_id, details_obj):
        """Saves a job."""

        # Check to see if Job is already saved. When a user saves a job in the fullscreen view, a back
        # press in the browswer will reveal the same job with the "save" button still clickable, which
        # can allow the user to click Save twice. This is why we need to check.

        if details_obj.get('cos_id'):
            already_saved_id = db.session.query(cls.id).filter(cls.user_id == user_id, cls.cos_id == details_obj['cos_id']).first()
            if already_saved_id:
                return already_saved_id[0]

        if details_obj.get('federal_contractor'):
            cls.coerce_fc_value(details_obj)

        # COS jobs posting times are weirdly in UTC time zone. I'm subtracting 5 hours to put it in 
        # Eastern or Central US time depending on Daylight Savings Time. 
        # This is not a perfect solution but improves the accuracy of dates and times for US users.
        if details_obj.get('date_posted'):
            new_date = datetime.strptime(details_obj['date_posted'], '%Y-%m-%d %I:%M %p') - timedelta(hours = 5)
            new_date_str = datetime.strftime(new_date, '%Y-%m-%d %I:%M %p')
            details_obj['date_posted'] = new_date_str

        if isinstance(details_obj.get('salary_min'), str):
            if details_obj['salary_min'] == '':
                details_obj['salary_min'] = None
            else:
                details_obj['salary_min'] = int(details_obj['salary_min'])

        if isinstance(details_obj.get('salary_max'), str):
            if details_obj['salary_max'] == '':
                details_obj['salary_max'] = None
            else:
                details_obj['salary_max'] = int(details_obj['salary_max'])

        job_to_save = cls(user_id = user_id)

        for key in details_obj:
            setattr(job_to_save, key, details_obj[key])
            
        # **********************need some error handling if not saved**********************
        db.session.add(job_to_save)
        db.session.commit()

        # If the job posting that is being saved is in the dashboard's new job postings list, remove job
        # postings from session so that a new list is retrieved upon next navigation to dashboard.
        if session.get('job_postings') and details_obj.get('cos_id'):
            for job in session['job_postings']['postings']:
                if job['JvId'] == details_obj['cos_id']:
                    session.pop('job_postings')
                    break

        return job_to_save.id

    @classmethod
    def edit_saved_job(cls, user_id, saved_job_id, details_obj):
        """Edits a saved job. Returns an object to be converted into a response object in app.py."""

        job_to_edit = cls.query.get(saved_job_id)
        if job_to_edit.user_id == user_id:
            print ('************** User Ids matched! *******************')

            if details_obj.get('federal_contractor'):
                cls.coerce_fc_value(details_obj)

            if isinstance(details_obj.get('salary_min'), str):
                if details_obj['salary_min'] == '':
                    details_obj['salary_min'] = None
                else:
                    details_obj['salary_min'] = int(details_obj['salary_min'])

            if isinstance(details_obj.get('salary_max'), str):
                if details_obj['salary_max'] == '':
                    details_obj['salary_max'] = None
                else:
                    details_obj['salary_max'] = int(details_obj['salary_max'])

            # try:
            for key in details_obj:
                setattr(job_to_edit, key, details_obj[key])

            db.session.add(job_to_edit)
            db.session.commit()
            # except: 
            #     return {'body': {'message': 'Sorry, we were unable to process your request. Please try again later!'}, 'status': 500}
            return {'body': {'message': 'Update Successful!'}, 'status': 200}
        else:
            return {'body': {'message': 'Unauthorized: This saved job is associated with another user.'}, 'status': 403}

    @classmethod
    def coerce_fc_value(cls, obj):
        """Replaces string value for federal contractor column with boolean value."""
   
        if obj['federal_contractor'] == "True":
            obj['federal_contractor'] = True
        if obj['federal_contractor'] == "False":
            obj['federal_contractor'] = False

        return obj

    @classmethod
    def delete_saved_job(cls, saved_job_id):
        """Deletes a saved job."""

        saved_job_to_delete = cls.query.get(saved_job_id)
        if saved_job_to_delete:
            db.session.delete(saved_job_to_delete)
            db.session.commit()

        return {'body': 'success!', 'status': 200}

    @classmethod
    def already_saved(cls, user_id, cos_id):
        """Checks to see if job found through API is already saved. Returns True or False."""

        id_if_exists = db.session.query(cls.id).filter(cls.user_id == user_id,
            cls.cos_id == cos_id).first()

        return id_if_exists != None

    @classmethod
    def already_saved_id(cls, user_id, cos_id):
        """Checks to see if job found through API is already saved. Returns JobSaved id or None."""

        id_if_exists = db.session.query(cls.id).filter(cls.user_id == user_id,
            cls.cos_id == cos_id).first()
        if id_if_exists:
            return id_if_exists[0]
        return id_if_exists

    @classmethod
    def get_dashboard_saved_jobs_list(cls, user_id):
        """creates shortened and prioritized saved_jobs list for dashboard."""

        return cls.query.filter_by(user_id = user_id, job_app = None).order_by(cls.id.desc()).limit(10).all()

    @classmethod
    def get_saved_job_by_id(cls, saved_job_id, translate_values=False):
        """Returns SavedJob object. Set translate_values to true to change shortened select input values to full values."""

        saved_job = cls.query.get(saved_job_id)

        if translate_values:
            saved_job = cls.translate_values(saved_job)

        return saved_job

    @classmethod
    def get_saved_job_obj_for_edit_form(cls, saved_job_id):
        """Returns SavedJob object. Strips time from date_posted."""

        saved_job = cls.query.get(saved_job_id)
        # saved_job.date_posted = date(saved_job.date_posted.year, saved_job.date_posted.month, saved_job.date_posted.day)

        return saved_job

    @classmethod
    def get_saved_job_obj_for_details_page(cls, saved_job_id):
        """Returns SavedJob object. Translates values from database values to human consumable values.
        Strips time from date_posted if not originating from COS API."""

        saved_job = cls.query.get(saved_job_id)
        saved_job_translated = cls.translate_values(saved_job)
        if not saved_job_translated.cos_id:
            saved_job_translated.date_posted = date(saved_job.date_posted.year, saved_job.date_posted.month, saved_job.date_posted.day)

        return saved_job_translated

    @classmethod
    def get_saved_jobs_for_list(cls, user_id, days_ago, include_applied):
        """Returns a list of saved jobs within <days_ago> and can or cannot <include_applied>.
        days_ago can be a number or 'all' (default, which means get all jobs no matter when saved)
        include_applied can be 'yes' or 'no' (default)"""

        if days_ago != 'all':
            date_of_x_days_ago = date.today() - timedelta(days = int(days_ago))
            if include_applied == 'no':
                return db.session.query(cls).filter(cls.user_id == user_id, cls.date_posted >= date_of_x_days_ago, cls.job_app == None).order_by(cls.id.desc()).all()
            else:
                return db.session.query(cls).filter(cls.user_id == user_id, cls.date_posted >= date_of_x_days_ago).order_by(cls.id.desc()).all()
        else:
            if include_applied == 'no':
                return db.session.query(cls).filter(cls.user_id == user_id, cls.job_app == None).order_by(cls.id.desc()).all()
            else:
                return db.session.query(cls).filter(cls.user_id == user_id).order_by(cls.id.desc()).all()

# --------------------------- app_factor -------------------------------------------------------------------------------------------------

app_factor = db.Table('app_factor',
    db.Column('job_app_id',
        db.Integer,
        db.ForeignKey('job_apps.id'),
        primary_key=True
    ),
    db.Column('factor_id',
        db.Integer,
        db.ForeignKey('factors.id'),
        primary_key=True
    )
)

# --------------------------- JobApp -------------------------------------------------------------------------------------------------

class JobApp(db.Model):

    __tablename__ = 'job_apps'

    id = db.Column(
        db.Integer,
        db.ForeignKey('saved_jobs.id'),
        primary_key=True
    )
    user_id = db.Column(db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    date_applied = db.Column(
        db.Date,
        nullable=False,
        default=date.today()
    )
    current_status = db.Column(
        db.Integer,
        nullable=False,
        default=2
    )
    # range: 0-8
    # values:
    #     2: Initial Screening
    #     3: Passed IS - No Interview Yet
    #     4: Interviewed - First Round
    #     5: Interviewed - Multiple Rounds
    #     6: Interviewed - Final Round
    #     7: Job Offer
    #     8: Hired
    #     0: Closed - Ghosted
    #     1: Closed - Rejection Notice
    # **Values are ordered by most exciting/interesting for prioritizing in lists.**
    furthest_status = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )
    # range: 0-6
    # values:
    #     0: Initial Screening
    #     1: Passed IS - No Interview Yet
    #     2: Interviewed - First Round
    #     3: Interviewed - Multiple Rounds
    #     4: Interviewed - Final Round
    #     5: Job Offer
    #     6: Hired
    last_status_change = db.Column(
        db.Date,
        nullable=False,
        default=date.today()
    )
    # Value will remain at 0 even when user marks "Interviewed - First Round" in current status.
    # User will only be asked to change this value when user marks a status value of 2 or higher.
    dpba = db.Column(db.Integer)
    # Days Posted Before Applying
    user_notes = db.Column(
        db.Text
    )
    job_hunt_id = db.Column(
        db.Integer,
        db.ForeignKey('job_hunts.id'),
        nullable = False
    )
    saved_job = db.relationship("SavedJob", back_populates="job_app")
    job_hunt = db.relationship("JobHunt", back_populates="job_apps")
    user = db.relationship('User', back_populates='job_apps')
    factors = db.relationship('Factor', secondary=app_factor, back_populates='job_apps')

    def __repr__(self):
        return f"<Job App #{self.id}: {self.saved_job.company}, {self.date_applied}>"

    def add_dpba(self):
        dpba = self.date_applied - self.saved_job.date_posted
        self.dpba = dpba.days

        return self

    def add_dsa_and_dssu(self):
        dsa = date.today() - self.date_applied
        self.dsa = dsa.days
        dssu = date.today() - self.last_status_change
        self.dssu = dssu.days

        return self

    def translate_values(self):
        status_translator = {0: 'Closed - Ghosted', 1: 'Closed - Rejection Notice', 2: 'Initial Screening', 3: 'Passed IS - No Interview Yet',
            4: 'Interviewed - First Round', 5: 'Interviewed - Multiple Rounds', 6: 'Interviewed - Final Round', 7: 'Job Offer', 8:'Hired'}
        self.current_status_translated = status_translator[self.current_status]
        self.furthest_status_translated = status_translator[self.furthest_status]

        return self

    def calculate_success_score(self):
        score_translator = [0, 0, 0, 3, 5, 10, 24, 50, 60]
        score = score_translator[self.furthest_status]
        if self.current_status == 1:
            score = score + 1
        self.ss = score

        return self

    @classmethod
    def add_job_app(cls, app_obj):
        """adds (reports) a job app to the database"""

        # check if job app already created for saved job
        if cls.query.get(app_obj['id']):
            return {'body': {'message': 'A job app associated with this job has already been created.'}, 'status': 409}

        app_to_add = cls()

        for key in app_obj:
            setattr(app_to_add, key, app_obj[key])

        # **********************need some error handling if not addd**********************
        db.session.add(app_to_add)
        db.session.commit()

        app_to_add_with_dpba = app_to_add.add_dpba()
        db.session.add(app_to_add_with_dpba)
        db.session.commit()

        return {'body': {'message': 'Job App Report Successful!'}, 'status': 200}
    
    @classmethod
    def get_dashboard_job_apps_list(cls, job_hunt_id):
        """creates shortened and prioritized saved_jobs list for dashboard"""

        return cls.query.filter_by(job_hunt_id = job_hunt_id).order_by(cls.current_status.desc(), cls.id.desc()).limit(8).all()

    @classmethod
    def check_if_applied(cls, saved_job_id):
        """Checks by save_job_id if there is an job app reported for this saved job. 
        Returns True if there is; returns False if there isn't."""

        return cls.query.get(saved_job_id) is not None

    @classmethod
    def get_all_job_apps_for_user(cls, job_hunt_id, translate_values):
        """Returns a list of all saved jobs associated with a user."""

        job_apps = cls.query.filter(job_hunt_id == job_hunt_id).order_by(cls.id.desc()).all()

        if translate_values:
            for app in job_apps:
                app = app.translate_values()

        return job_apps

    @classmethod
    def get_job_apps_for_list(cls, user_id, job_hunt_id, translate_values):
        """Returns a list of all saved jobs associated with a user."""

        if job_hunt_id >= 0:
            job_apps = db.session.query(cls).filter(cls.job_hunt_id == job_hunt_id).order_by(cls.id.desc()).all()
        elif job_hunt_id == -1:
            active_hunt_tuples = JobHunt.get_active_job_hunt_ids(user_id)
            active_hunt_ids = [tup[0] for tup in active_hunt_tuples]
            job_apps = db.session.query(cls).filter(cls.job_hunt_id.in_(active_hunt_ids)).order_by(cls.id.desc()).all()
        else:
            job_apps = db.session.query(cls).filter(cls.user_id == user_id).order_by(cls.id.desc()).all()

        for app in job_apps:
            app = app.add_dsa_and_dssu()
            app = app.calculate_success_score()
        if translate_values:
            for app in job_apps:
                app = app.translate_values()

        return job_apps

    @classmethod
    def get_job_app_by_id(cls, job_app_id, translate_values=False):

        job_app = cls.query.get(job_app_id)
        job_app = job_app.add_dsa_and_dssu()
        job_app = job_app.calculate_success_score()
        if translate_values:
            job_app = job_app.translate_values()

        return job_app

    @classmethod
    def edit_job_app(cls, user_id, job_app_id, details_obj):
        """Edits a job app. Returns an object to be converted into a response object in app.py."""

        app_to_edit = cls.query.get(job_app_id)
        if app_to_edit.user_id == user_id:
            print ('************** User Ids matched! *******************')

            if app_to_edit.current_status != details_obj.get('current_status', app_to_edit.current_status):
                details_obj['last_status_change'] = date.today()

                if int(details_obj['current_status']) > 1:
                    details_obj['furthest_status'] = details_obj['current_status']

            try:
                for key in details_obj:
                    if not details_obj[key]:
                        details_obj[key] = None
                    setattr(app_to_edit, key, details_obj[key])
                db.session.add(app_to_edit)
                db.session.commit()
            except: 
                return {'body': {'message': 'Sorry, we were unable to process your request. Please try again later!'}, 'status': 500}
            return {'body': {'message': 'Update Successful!'}, 'status': 200}
        else:
            return {'body': {'message': 'Unauthorized: This saved job is associated with another user.'}, 'status': 403}

    @classmethod
    def delete_job_app(cls, user_id, job_app_id):
        """Deletes a job app. Returns an object to be converted into a response object in app.py."""

        app_to_delete = cls.query.get(job_app_id)
        job_hunt_id = app_to_delete.job_hunt_id
        if app_to_delete.user_id == user_id:
            print ('************** User Ids matched! *******************')

            db.session.delete(app_to_delete)
            db.session.commit()

        return {'body': job_hunt_id, 'status': 200}

# --------------------------- Factor -------------------------------------------------------------------------------------------------

class Factor(db.Model):

    __tablename__ = 'factors'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    name = db.Column(
        db.String(50),
        nullable=False
    )
    job_hunt_id = db.Column(
        db.Integer,
        db.ForeignKey('job_hunts.id'),
        nullable = False
    )
    job_hunt = db.relationship("JobHunt", back_populates="factors")
    job_apps = db.relationship("JobApp", secondary=app_factor, back_populates="factors")

    def __repr__(self):
        return f"<Factor #{self.id}: {self.name}>"

    @classmethod
    def add_factors(cls, factors_to_add, current_user_id):
        """Accepts a list of factor objects to add to the database."""

        new_factor_id_list = []

        if (factors_to_add):
            user_id_associated_with_job_hunt = db.session.query(JobHunt.user_id).filter_by(id = factors_to_add[0]['job_hunt_id']).first()[0]
            if (current_user_id != user_id_associated_with_job_hunt):
                return {'body': {'message': 'You are not authorized to do this.'}, 'status': 401}

            new_factor_list = []

            for factor in factors_to_add:
                new_factor = cls(job_hunt_id = factor['job_hunt_id'], name = factor['name'])
                new_factor_list.append(new_factor)
                db.session.add(new_factor)
            db.session.commit()
            new_factor_id_list = [x.id for x in new_factor_list]

        return {'body': new_factor_id_list, 'status': 200}

    @classmethod
    def add_factors_from_name_list(cls, factors_to_add, job_hunt_id, current_user_id):
        """Accepts a list of factor names to add to the database."""

        new_factor_id_list = []

        if (factors_to_add):
            user_id_associated_with_job_hunt = db.session.query(JobHunt.user_id).filter_by(id = job_hunt_id).first()[0]
            if (current_user_id != user_id_associated_with_job_hunt):
                return {'body': {'message': 'You are not authorized to do this.'}, 'status': 401}

            new_factor_list = []

            for factor in factors_to_add:
                new_factor = cls(job_hunt_id = job_hunt_id, name = factor)
                new_factor_list.append(new_factor)
                db.session.add(new_factor)
            db.session.commit()
            new_factor_id_list = [x.id for x in new_factor_list]

        return {'body': new_factor_id_list, 'status': 200}

    @classmethod
    def associate_factors_from_dict(cls, factors_dict, current_user_id):
        """Accepts a dict of factors to add to the database."""

        user_id_associated_with_job_app = db.session.query(SavedJob.user_id).filter_by(id = factors_dict['savedJobId']).first()[0]
        if (current_user_id != user_id_associated_with_job_app):
            return {'body': 'You are not authorized to do this.', 'status': 401}

        factors_list = [cls.query.get(factorId) for factorId in factors_dict['allFactorsIdArray']]
        app_to_associate_factors_with = JobApp.query.get(factors_dict['savedJobId'])
        app_to_associate_factors_with.factors.extend(factors_list)
        db.session.commit()

        return {'body': 'success!', 'status': 200}

    @classmethod
    def associate_factors_from_id_list(cls, factors_id_list, job_app_id, current_user_id):
        """Accepts a dict of factors to add to the database."""

        user_id_associated_with_job_app = db.session.query(SavedJob.user_id).filter_by(id = job_app_id).first()[0]
        if (current_user_id != user_id_associated_with_job_app):
            return {'body': 'You are not authorized to do this.', 'status': 401}

        factors_list = [cls.query.get(factorId) for factorId in factors_id_list]
        app_to_associate_factors_with = JobApp.query.get(job_app_id)
        app_to_associate_factors_with.factors = factors_list
        db.session.commit()

        return {'body': 'success!', 'status': 200}