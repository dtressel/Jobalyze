from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    email = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )
    username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )
    password = db.Column(
        db.Text,
        nullable=False
    )
    first_name = db.Column(
        db.String(30)
    )
    last_name = db.Column(
        db.String(30)
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
    # range: 0-7
    # values:
    #     0: 1-10 employees.
    #     1: 11-50 employees.
    #     2: 51-200 employees.
    #     3: 201-500 employees.
    #     4: 501-1000 employees.
    #     5: 1001-5000 employees.
    #     6: 5001-10,000 employees.
    #     7: 10,001+ employees.

    job_type = db.Column(
        db.Integer
    )
    # range: 0-4
    # values:
    #     0: Full-time
    #     1: Part-time
    #     2: Contract
    #     3: Internship
    #     4: Volunteer

    experience_level = db.Column(
        db.String(100)
    )
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
        db.String(500)
    )
    user_notes = db.Column(
        db.Text
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable = False
    )
    user = db.relationship('User', back_populates='saved_jobs')
    job_app = db.relationship("JobApp", back_populates="user", uselist=False, cascade="all, delete")

class JobHunt(db.Model):

    __tablename__ = 'job_hunts'

    id = db.Column(
        db.Integer,
        primary_key=True
    )
    job_title_desired = db.Column(
        db.Text,
        nullable=False
    )
    date_begun = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
    )
    status = db.Column(db.Integer)
    # range: 0-2
    # values:
    #     0: Actively Applying
    #     1: Closed, Hired
    #     2: Closed, Abandoned
    
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
    hired_by_app_id = db.Column(
        db.Integer,
        db.ForeignKey('job_apps.id')
    )
    user = db.relationship('User', back_populates='job_hunts')
    job_apps = db.relationship('JobApp', back_populates='job_hunt', cascade="all, delete")
    strategies = db.relationship("Strategy", back_populates="job_hunt", cascade="all, delete")
    hired_by = db.relationship('JobApp')


app_strategy = db.Table('app_strategy',
    db.Column('job_app_id',
        db.Integer,
        db.ForeignKey('saved_jobs.id'),
        primary_key=True
    ),
    db.Column('strategy_id',
        db.Integer,
        db.ForeignKey('strategies.id'),
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
    strategies = db.relationship('Strategy', secondary=app_strategy, back_populates='job_apps')

class Strategy(db.Model):

    __tablename__ = 'strategies'

    id = db.Column(
        db.Integer,
        db.ForeignKey('saved_jobs.id'),
        primary_key=True
    )
    name = db.Column(
        db.String(100),
        nullable=False
    )
    job_hunt_id = db.Column(
        db.Integer,
        db.ForeignKey('job_hunts.id'),
        nullable = False
    )
    job_hunt = db.relationship("JobHunt", back_populates="strategies")
    job_apps = db.relationship("JobApp", secondary=app_strategy, back_populates="strategies")


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)