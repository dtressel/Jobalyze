import os

from flask import Flask, render_template, redirect, session
# For auth:
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, connect_db, User
from forms import RegistrationForm, UserLoginForm, UserEditForm

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
        return render_template('home_anon.html', current_user=current_user)
    else:
        return render_template('home_user.html', current_user=current_user)

# Authorization:

@app.route('/register', methods=["GET", "POST"])
def register():
    """Register User"""

    if current_user:
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

        return redirect('/')
    else:
        return render_template('register.html', form = form, current_user=current_user)
