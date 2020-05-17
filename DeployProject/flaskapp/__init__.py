from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_images import Images
import os
from flask_mail import Mail
from itsdangerous import URLSafeSerializer
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__,static_folder='static',template_folder='templates')
SECRET_KEY_JWT = 'cb5a0fb869b53f9aec4ac70af0a2143a'
app.config['SECRET_KEY'] = 'beaa4c2cea1c931323b8eee58104b0cc'

engine = create_engine('mysql://krish:12345@localhost:3306/deploy', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Here login is the name of the route login method
login_manager.login_message_category = 'info'
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'kishorekumar131646@gmail.com'
app.config['MAIL_PASSWORD'] = 'Kishorekumar@646'
mail = Mail(app)
images = Images(app)
auth_s = URLSafeSerializer(app.config['SECRET_KEY'], "auth")


from flaskapp import views


def init_db():
   
    from flaskapp import models
    Base.metadata.create_all(bind=engine)