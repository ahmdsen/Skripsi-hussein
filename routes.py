from flask import render_template, url_for, flash, redirect, request
from app import app, db
from forms import CitizenForm
from models import User, Citizen
from forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('home.html', title='Home')
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
    return render_template('users/users.html', users=users)

@app.route('/citizens', methods=['GET', 'POST'])
def citizens():
    citizens = Citizen.query.all()
    return render_template('citizens/citizens.html', citizens=citizens)

@app.route('/citizen/add', methods=['GET', 'POST'])
def add_citizen():
    form = CitizenForm()
    if form.validate_on_submit():
        citizen = Citizen(
            nama=form.nama.data,
            alamat=form.alamat.data,
            pendapatan=form.pendapatan.data,
            status_rumah_tinggal=form.status_rumah_tinggal.data,
            status_pekerjaan=form.status_pekerjaan.data,
            kondisi_rumah=form.kondisi_rumah.data,
            jumlah_anggota_keluarga=form.jumlah_anggota_keluarga.data,
            status_bantuan=form.status_bantuan.data,
            informasi_tambahan=form.informasi_tambahan.data
        )
        db.session.add(citizen)
        db.session.commit()
        flash('Citizen added successfully!', 'success')
        return redirect(url_for('citizens'))
    return render_template('citizens/add_citizen.html', form=form)

@app.route('/citizen/edit/<int:id>', methods=['GET', 'POST'])
def edit_citizen(id):
    citizen = Citizen.query.get_or_404(id)
    form = CitizenForm(obj=citizen)
    if form.validate_on_submit():
        citizen.nama = form.nama.data
        citizen.alamat = form.alamat.data
        citizen.pendapatan = form.pendapatan.data
        citizen.status_rumah_tinggal = form.status_rumah_tinggal.data
        citizen.status_pekerjaan = form.status_pekerjaan.data
        citizen.kondisi_rumah = form.kondisi_rumah.data
        citizen.jumlah_anggota_keluarga = form.jumlah_anggota_keluarga.data
        citizen.status_bantuan = form.status_bantuan.data
        citizen.informasi_tambahan = form.informasi_tambahan.data
        db.session.commit()
        flash('Citizen updated successfully!', 'success')
        return redirect(url_for('citizens'))
    return render_template('citizens/edit_citizen.html', form=form)

@app.route('/citizen/delete/<int:id>', methods=['POST'])
def delete_citizen(id):
    citizen = Citizen.query.get_or_404(id)
    db.session.delete(citizen)
    db.session.commit()
    flash('Citizen deleted successfully!', 'success')
    return redirect(url_for('citizens'))

@app.route('/assistance')
@login_required
def assistance():
    return render_template('assistance.html', title='Assistance')

@app.route('/feedback')
@login_required
def feedback():
    return render_template('feedback.html', title='Feedback')

@app.route('/users/add', methods=['GET', 'POST'])
@login_required  # Ensure only logged-in users can access this route
def add_user():
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
            flash('User added successfully!', 'success')
            return redirect(url_for('users'))  # Redirect to a route where all users are listed
    return render_template('users/add_user.html', title='Add User', form=form)

@app.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = RegistrationForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.nama_lengkap = form.nama_lengkap.data
        if form.password.data:  # Only update password if a new one is provided
            user.password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('users'))  # Redirect to a route where all users are listed
    return render_template('users/edit_user.html', title='Edit User', form=form)

@app.route('/users/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('users'))  # Redirect to a route where all users are listed

