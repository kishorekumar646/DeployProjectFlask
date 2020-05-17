from flaskapp import db_session, Base, login_manager
from flask_login import UserMixin
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Table, Boolean
from werkzeug.security import generate_password_hash, check_password_hash
from .exception import Unauthenticated


@login_manager.user_loader
def load_user(user_id):
    print('login')
    return User.query.get(int(user_id))


class User(Base,UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), nullable=False)
    email = Column(String(120), nullable=False)
    password_hash = Column(String(128))
    is_active = Column(Boolean,default=False)

    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.is_active = False

    def set_password(self, password):
        password = self.password_hash = generate_password_hash(password)
        return password

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def save(self, user):
        try:
            db_session.add(user)
            db_session.commit()
            return "successfully created user"

        except Exception as e:
            return "ERROR"

    def __repr__(self):
        return '<User {}>'.format(self.username)


def authenticate_user(email, password):
    
    user = User.query.filter_by(email=email).first()

    if user is None:
        print("user : ", user)
        return False

    if user.check_password(password=password):
        print('ok')
        return user

    return False
