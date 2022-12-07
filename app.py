import os

from flask import Flask, render_template, redirect, flash, request, abort, session
# For auth:
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from is_safe_url import is_safe_url
from models import db, connect_db, User
from forms import RegistrationForm, LoginForm, UserEditForm

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///jobalyze'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "aji32ojfuJHwp")

connect_db(app)

# For auth:
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

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
        new_user = User.create_user(
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
            if not is_safe_url(next):
                return abort(400)

            return redirect(next or '/')
        else:
            form.password.errors = ['Incorrect username or password.']
    return render_template('login.html', form=form)
