from flask import render_template, url_for, flash, redirect, request
from app import app, db
from models import User
from forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        return render_template('home.html')
    else:
        form = LoginForm()
        return render_template('login.html',form=form, remember=form.remember.data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash('Email already registered. Please use a different email.', 'danger')
        else:
            hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
            user = User(username=form.username.data, email=form.email.data, password=hashed_password, nama_lengkap=form.nama_lengkap.data)
            db.session.add(user)
            db.session.commit()
            flash('Your account has been created!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)
