# import flask - from the package import class
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask import render_template
import os

db = SQLAlchemy()

# create a function that creates a web application
# a web server will run this web application


def pageNotFound(e):
    return render_template('404.html'), 404


def create_app():

    # this is the name of the module/package that is calling this app
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'ThankTheLordsThisSemesterIsEnding'

    app.register_error_handler(404, pageNotFound)

    # set the app configuration data

    # Database initlisation for local
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///web_app.sqlite'

    # Database initlisation for Heroku
    # app.config.from_mapping(
    #     SQLALCHEMY_DATABASE_URI=os.environ['DATABASE_URL']
    # )

    # initialize db with flask app

    db.init_app(app)

    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    bootstrap = Bootstrap(app)

    # initialize the login manager
    login_manager = LoginManager()

    # set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    # shaun updated-30/9/2019 OPEN
    from. import items
    app.register_blueprint(items.bp)
    # shaun updated-30/9/2019 CLOSE

    return app
