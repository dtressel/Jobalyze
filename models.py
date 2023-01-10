from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table
from flask_login import UserMixin

bcrypt = Bcrypt()
db = SQLAlchemy()


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
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
    )
    saved_jobs = db.relationship('SavedJob', back_populates='user', cascade="all, delete")
    job_hunts = db.relationship('JobHunt', back_populates='user', cascade="all, delete")

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    def current_hunt(self):
        """Find a users most recent job hunt"""
        if self.job_hunts:
            return self.job_hunts[-1]
        return None

    @classmethod
    def signup(cls, email, username, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = cls(
            email=email,
            username=username,
            password=hashed_pwd
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate_user(cls, username, password):
        """Authenticates user on log in and returns user instance"""

        user = cls.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

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
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
    )
    date_posted = db.Column(
        db.DateTime
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
    last_cos_update = db.Column(db.DateTime,
        default=datetime.utcnow())
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable = False
    )
    exclude = db.Column(db.Boolean,
        default=False)
        # exclude from saved job list?
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
            self.company_size = cs_translator[self.company_size]

        # Salary range locale string translation done in job-details-saved.js

        if self.job_type:
            jt_translator = {'f': 'Full-time', 'p': 'Part-time', 'c': 'Contract', 'i': 'Internship', 'v': 'Volunteer'}
            self.job_type = jt_translator[self.job_type]

        if self.federal_contractor != None:
            fc_translator = {True: 'Yes', False: 'No'}
            self.federal_contractor = fc_translator[self.federal_contractor]

        if self.experience_level:
            el_translator = {'i': 'Internship', 'e': 'Entry level', 'a': 'Associate',
            'm': 'Mid-Senior level', 'd': 'Director', 'x': 'Executive'}
            self.experience_level = el_translator[self.experience_level]

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
        return job_to_save.id

    @classmethod
    def edit_saved_job(cls, user_id, saved_job_id, details_obj):
        """Edits a saved job. Returns an object to be converted into a response object in app.py."""

        saved_job = cls.query.get(saved_job_id)
        if saved_job.user_id == user_id:
            print ('************** User Ids matched! *******************')

            if details_obj.get('federal_contractor'):
                cls.coerce_fc_value(details_obj)

            try:
                job_to_edit = cls.query.get(saved_job_id)
                for key in details_obj:
                    setattr(job_to_edit, key, details_obj[key])
                db.session.add(job_to_edit)
                db.session.commit()
            except: 
                return {'body': {'message': 'Sorry, we were unable to process your request. Please try again later!'}, 'status': 500}
            return {'body': {'message': 'Update Successful!'}, 'status': 200}
        else:
            return {'body': {'message': 'Unauthorized: This saved job is associated with another user.'}, 'status': 403}

    @classmethod
    def coerce_fc_value(cls, obj):
        """Replaces string value for federal contractor column with boolean value."""

        if obj['federal_contractor'] == "-":
            obj['federal_contractor'] = None       
        if obj['federal_contractor'] == "True":
            obj['federal_contractor'] = True
        if obj['federal_contractor'] == "False":
            obj['federal_contractor'] = False

        return obj

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
        """creates shortened and prioritized saved_jobs list for dashboard"""

        return cls.query.filter_by(user_id = user_id).order_by(cls.id.desc()).limit(10)

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
        default=25)
    non_us = db.Column(db.Boolean,
        nullable=False,
        default=False)
    remote = db.Column(db.Boolean,
        nullable=False,
        default=False)
    date_begun = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
    )
    hired_by_goal_date = db.Column(db.DateTime)
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
    #     h: Closed, Hired
    #     c: Closed, Abandoned
    
    description = db.Column(
        db.Text
    )
    date_closed = db.Column(
        db.DateTime
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
    def get_active_job_hunts(cls, user_id):
        """Returns a list of active job hunts for a user."""

        return db.session.query(cls).filter(cls.user_id == user_id, cls.status == 'a').order_by(cls.id.desc()).all()

    @classmethod
    def getFactors(cls, job_hunt_id):
        """Returns factors for a given job hunt id"""

        job_hunt = cls.query.get(job_hunt_id)
        factors_list = [{'id': x.id, 'name': x.name} for x in job_hunt.factors]

        return factors_list

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

class JobApp(db.Model):

    __tablename__ = 'job_apps'

    id = db.Column(
        db.Integer,
        db.ForeignKey('saved_jobs.id'),
        primary_key=True
    )
    user_id = db.Column(db.Integer,
        nullable=False)
    date_applied = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
    )
    current_status = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )
    # range: 0-5
    # values:
    #     0: Initial Screening
    #     1: Interviewed - First Round
    #     2: Interviewed - Multiple Rounds
    #     3: Interviewed - Final Round
    #     4: Job Offer
    #     5: Hired

    interviews = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )
    # Value will remain at 0 even when user marks "Interviewed - First Round" in current status.
    # User will only be asked to change this value when user marks a current_status value of 2 or higher.

    furthest_status = db.Column(
        db.Integer,
        nullable=False,
        default=0
    )
    date_closed = db.Column(
        db.DateTime
    )
    job_hunt_id = db.Column(
        db.Integer,
        db.ForeignKey('job_hunts.id'),
        nullable = False
    )
    saved_job = db.relationship("SavedJob", back_populates="job_app")
    job_hunt = db.relationship("JobHunt", back_populates="job_apps")
    factors = db.relationship('Factor', secondary=app_factor, back_populates='job_apps')

    def __repr__(self):
        return f"<Job App #{self.id}: {self.saved_job.company}, {self.current_status}>"

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
        return {'body': {'message': 'Job App Report Successful!'}, 'status': 200}
    
    @classmethod
    def get_dashboard_job_apps_list(cls, user_id):
        """creates shortened and prioritized saved_jobs list for dashboard"""

        return cls.query.filter_by(user_id = user_id).order_by(cls.date_applied.desc()).limit(8)

    @classmethod
    def check_if_applied(cls, saved_job_id):
        """Checks by save_job_id if there is an job app reported for this saved job. 
        Returns True if there is; returns False if there isn't."""

        return cls.query.get(saved_job_id) is not None

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
        """Accepts a list of factors to add to the database."""

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
    def associate_factors(cls, associate_factors_dict, current_user_id):
        """Accepts a list of factors to add to the database."""

        user_id_associated_with_job_app = db.session.query(SavedJob.user_id).filter_by(id = associate_factors_dict['savedJobId']).first()[0]
        if (current_user_id != user_id_associated_with_job_app):
            return {'body': 'You are not authorized to do this.', 'status': 401}

        factors_list = [cls.query.get(factorId) for factorId in associate_factors_dict['allFactorsIdArray']]
        app_to_associate_factors_with = JobApp.query.get(associate_factors_dict['savedJobId'])
        import pdb; pdb.set_trace()
        app_to_associate_factors_with.factors.extend(factors_list)
        db.session.commit()
        import pdb; pdb.set_trace()

        return {'body': 'success!', 'status': 200}

def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)