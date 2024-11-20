from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_session import Session
from flask_mail import Mail
from app.config import Config

############################### Creating Instances  #########################################

db = SQLAlchemy() #SQLAlchemy db instance
bcrypt = Bcrypt() #to generate password hash
login_manager =  LoginManager() #instance of LoginManager import from flask_login
login_manager.login_view = 'auth.login' #we need to tell the function where the login view is created.login is function name of the route
login_manager.login_message_category = 'info' #just adding some bootstrap class to show the messages in a better way.
mail = Mail()
session = Session()

#############################################################################################
################################ Create APP function  #######################################
#############################################################################################

def create_app(config_class= Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app=app)
    bcrypt.init_app(app=app)
    login_manager.init_app(app=app)
    mail.init_app(app=app)
    session.init_app(app=app)

    from app.routes.auth import auth_bp
    from app.routes.main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app