from flask import (
    Blueprint, flash, render_template, request, url_for, redirect
)
from .models import User
from .forms import LoginForm, RegisterForm
from . import db
from flask_login import login_user, logout_user

# for password storage
from werkzeug.security import generate_password_hash, check_password_hash

# create a blueprint
bp = Blueprint('auth', __name__)

# -------------------
# login page
# -------------------
@bp.route('/login', methods=['GET', 'POST'])
def login():
    # load the login form
    form = LoginForm()
    error = None

    # if the user pressed login
    if(form.validate_on_submit()):
        # pull the user name and password the user entered in the form
        user_name = form.name.data
        password = form.password_hash.data

        # pulls the data for a user with that name
        u1 = User.query.filter_by(name=user_name).first()

        # if there is no user with that name
        if u1 is None:
            error = 'Incorrect user name'
        # check the password - notice password hash function
        # takes the hash and password
        elif not check_password_hash(u1.password_hash, password):
            error = 'Incorrect password'

        # if the login details are correct
        if error is None:
            # all good, set the login_user
            login_user(u1, force=True)
            return redirect(url_for('main.index'))
        else:
            # show the error messages to the user with flash
            print(error)
            flash(error)

    # it comes here when it is a get method
    return render_template('user.html', form=form, heading='Login')

# -------------------
# register page
# -------------------
@bp.route('/register', methods=['GET', 'POST'])
def register():
    # load the register form
    form = RegisterForm()
    error = None

    # if the register button is pressed
    if form.validate_on_submit():
        # get username, password, email, phone number and address from the form
        uname = form.name.data
        pwd = form.password.data
        email = form.emailid.data
        phone = form.phone.data
        address = form.location.data
        # don't store the password - create password hash
        pwd_hash = generate_password_hash(pwd)

        # query the database for any user with the username or email provided
        u1 = User.query.filter_by(name=uname).first()
        e1 = User.query.filter_by(emailid=email).first()

        # if the username is taken, provide the user with a useful error message
        if u1 != None:
            error = 'Username ' + uname + ' is taken, please choose another username.'

        # if the email has already been used, provide the user with a useful error message
        elif e1 != None:
            error = 'Email ' + email + ' has already been used.'

        # if the username and email are unique
        if error is None:
            # commit the user details to the DB
            new_user = User(name=uname, emailid=email, phone_no=phone,
                            password_hash=pwd_hash, location=address)
            db.session.add(new_user)
            db.session.commit()

            # credirect the user to login
            return redirect(url_for('auth.login'))
        else:
            print(error)
            # print the error messages on screen
            flash(error)

    return render_template('user.html', form=form, heading='Register')

# -------------------
# logout page
# -------------------
@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
