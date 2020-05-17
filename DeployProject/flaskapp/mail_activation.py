from flask_mail import Message
from flaskapp import mail
from flask import render_template, url_for, flash, redirect,request
import jwt


def send_reset_email(user,received_token):
    token = received_token  
    msg = Message('Password Reset Request',
                  sender='kishorekumar131646@gmail.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}
    If you did not make this request then simply ignore this email and no changes will be made.
    '''
    mail.send(msg)

def register_mail_activate(user,received_token):
    token = received_token
    try:
        msg = Message('Account activation Request',
                    sender='kishorekumar131646@gmail.com',
                    recipients=[user.email])
        msg.body = f'''To activate your account, visit the following link:
        {url_for('register_activate', token=token, _external=True)}
        If you did not make this request then simply ignore this email and no changes will be made.
        '''
        mail.send(msg)
    except jwt.ExpiredSignatureError:
        pass
    return token