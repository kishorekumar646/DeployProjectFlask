import jwt
import datetime
from flaskapp import app, auth_s, SECRET_KEY_JWT
from flaskapp.models import User
from jwt.exceptions import ExpiredSignatureError
from flaskapp import app, db_session, bcrypt, mail
from flask import flash, redirect, url_for


def token_activation(username, email):
    data = {
        'username': username,
        'email': email,
        'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=20)
    }
    # here it generates the token with the data provided along with secret key and default algorithm of django
    token_generated = jwt.encode(
        data, key=SECRET_KEY_JWT, algorithm='HS256').decode('utf-8')
    # token = auth_s.dumps(data)
    return token_generated


def validate_token(token):
    result = None
    try:
        # data = auth_s.loads(token)
        # print(data)
        data = jwt.decode(token, SECRET_KEY_JWT)
        username = data["username"]
        result = username
    except ExpiredSignatureError:
        pass
    return result


def register_validate_token(token):
    result = None
    try:
        # validate_token(token)
        data = jwt.decode(token, SECRET_KEY_JWT)
        token_username = data['username']
        token_email = data['email']
        user = User.query.filter_by(username=token_username,email=token_email).first()
        print("user = ", user)
        if user is not None:
            update = User.query.filter_by(id=user.id).update({User.is_active: True})
            user.save(user)
            flash('Your account has been created! You are now able to log in', 'success')
            return redirect(url_for('login'))
        else:
            flash('Not a valid user, Kindly register', 'danger')
            return redirect(url_for('register'))
        return redirect(url_for('register'))

    except ExpiredSignatureError:
        flash('Your Session has expired. Please register again', 'danger')
        return redirect(url_for('register'))

    return result
