from flaskapp import app, db_session, bcrypt, mail, auth_s, login_manager
from flaskapp.models import User, authenticate_user
from flask import render_template, url_for, flash, redirect, request, session, make_response
from flaskapp.forms import RegistrationForm, LoginForm, ResetPasswordForm, RequestResetForm
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp.token import token_activation, validate_token, register_validate_token
import redis
from flask_mail import Message
from flaskapp.mail_activation import register_mail_activate, send_reset_email
from jwt.exceptions import ExpiredSignatureError
from itsdangerous import URLSafeSerializer

redis_client = redis.Redis(host="localhost", port=6379)


@app.route("/home")
@login_required
def home():
    form = LoginForm()
    token = request.cookies.get('token')
    if token:
        redis_token = redis_client.get(token)
        if redis_token:
            username = validate_token(redis_token)
            if username:
                user = User.query.filter_by(username=username).first()
                return render_template('home.html', title='Account')
            else:

                return render_template('login.html', title='Login', form=form)
        else:

            return render_template('login.html', title='Login', form=form)
    else:

        return render_template('login.html', title='Login', form=form)
    return render_template('login.html', title='Login', form=form)


@app.route("/account")
@login_required
def account():
    form = LoginForm()
    token = request.cookies.get('token')
    if token:
        redis_token = redis_client.get(token)
        if redis_token:
            username = validate_token(redis_token)
            if username:
                user = User.query.filter_by(username=username).first()
                return render_template('account.html', title='Account')
            else:

                return render_template('login.html', title='Login', form=form)
        else:

            return render_template('login.html', title='Login', form=form)
    else:

        return render_template('login.html', title='Login', form=form)
    return render_template('login.html', title='Login', form=form)


@app.route("/about")
@login_required
def about():
    form = LoginForm()
    token = request.cookies.get('token')
    if token:
        redis_token = redis_client.get(token)
        if redis_token:
            username = validate_token(redis_token)
            if username:
                user = User.query.filter_by(username=username).first()
                return render_template('about.html', title='Account')
            else:

                return render_template('login.html', title='Login', form=form)
        else:

            return render_template('login.html', title='Login', form=form)
    else:

        return render_template('login.html', title='Login', form=form)
    return render_template('login.html', title='Login', form=form)


@app.route("/contact")
@login_required
def contact():
    form = LoginForm()
    token = request.cookies.get('token')
    if token:
        redis_token = redis_client.get(token)
        if redis_token:
            username = validate_token(redis_token)
            if username:
                user = User.query.filter_by(username=username).first()
                return render_template('contact.html', title='Account')
            else:

                return render_template('login.html', title='Login', form=form)
        else:

            return render_template('login.html', title='Login', form=form)
    else:

        return render_template('login.html', title='Login', form=form)
    return render_template('login.html', title='Login', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(password=form.password.data)
        user.save(user)
        token = token_activation(user.username, user.email)
        register_mail_activate(user, token)
        flash('An email has been sent with instructions to activate your account.', 'info')

    return render_template('register.html', title='Register', form=form)


@app.route("/register_activate/<token>", methods=['GET', 'POST'])
def register_activate(token):

    received_token = token
    return_token = register_validate_token(received_token)
    return return_token


@app.route("/")
@app.route("/login", methods=['GET', 'POST'])
def login():

    try:
        if current_user.is_authenticated:
            return redirect(url_for('home'))

        form = LoginForm()
        if form.validate_on_submit():

            try:
                user = authenticate_user(
                    email=form.email.data, password=form.password.data)

                if user:

                    if user.is_active:
                        login_user(user, remember=form.remember.data)
                        print('log')
                        next_page = request.args.get('next')
                        print(next_page)
                        # Generating JWT token
                        token = token_activation(user.username, user.email)
                        # Storing token into redis cache
                        redis_client.set(token, token)
                        redr = redirect(next_page) if next_page else redirect(
                            url_for('home'))
                        redr.set_cookie('token', token)
                        return redr

                    else:
                        flash(
                            'Login Unsuccessful. Please check your email and activate account', 'danger')

                else:
                    raise Exception

            except Exception:
                flash('Please check your login details and try again.', 'danger')

        return render_template('login.html', title='Login', form=form)

    except ExpiredSignatureError:
        return render_template('register.html', title='Register', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/forgot_password", methods=['GET', 'POST'])
def reset_request():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form = RequestResetForm()
    if request.method == "POST":
        email = form.email
        if form.validate_on_submit():
            print('ok')
            user = form.validate_reset_email(email)
            if user:
                token = token_activation(user.username, user.email)
                send_reset_email(user, token)
                flash(
                    'An email has been sent with instructions to reset your password.', 'info')

            else:
                flash(
                    'There is no account with that email. You must register first.', 'info')

        return render_template('reset_request.html', title='Reset Password', form=form)

    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    username = validate_token(token)

    if username:
        user = User.query.filter_by(username=username).first()

        form = ResetPasswordForm()
        if request.method == "POST":
            if form.validate_on_submit():
                print('post')
                if form.password.data == form.confirm_password.data:
                    update = User.query.filter_by(id=user.id).update(
                        {User.password_hash: user.set_password(password=form.password.data)})
                    user.save(user)
                    print(update)
                    flash(
                        'Your password has been updated! You are now able to log in', 'success')
                    return redirect(url_for('login'))

                else:
                    flash('Password miss match', 'danger')

        return render_template('reset_token.html', title='Reset Password', form=form)

    return render_template('forgot_password.html', title='Reset Password', form=form)
