import logging
import os
import csv
from flask import render_template, url_for, flash, redirect, request
from app import app, db
from werkzeug.utils import secure_filename
from forms import CitizenForm
from models import User, Citizen
from forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.naive_bayes import CategoricalNB
from sklearn.metrics import classification_report
from sklearn.impute import SimpleImputer
import re

logging.basicConfig(level=logging.DEBUG)

app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    logging.debug(f"Editing citizen with ID: {id}")
    citizen = Citizen.query.get_or_404(id)
    form = CitizenForm(obj=citizen)
    if form.validate_on_submit():
        logging.debug("Form validated successfully")
        try:
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
        except Exception as e:
            logging.error(f"Error updating citizen: {e}")
            flash('An error occurred while updating the citizen.', 'danger')
    return render_template('citizens/edit_citizen.html', form=form, citizen=citizen)

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
    return render_template('assistance/assistance.html', title='Assistance')

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
    return render_template('users/add_users.html', form=form)

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
    return render_template('users/edit_users.html', form=form, user=user)

@app.route('/users/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('users'))  # Redirect to a route where all users are listed

def process_csv_file(file_path):
    df = pd.read_csv(file_path, delimiter=';')
    
    # Handle numeric columns with non-numeric characters (e.g., thousand separators)
    numeric_columns = ['jumlah_anggota', 'pendapatan_gaji']
    
    for col in numeric_columns:
        df[col] = df[col].astype(str).str.replace(r'\D', '').astype(float)  # Convert to string first, then remove non-numeric characters and convert to float
    
    # Handle missing values with mean for numeric columns
    imputer = SimpleImputer(strategy='mean')
    df[numeric_columns] = imputer.fit_transform(df[numeric_columns])
    
    # Handle categorical columns
    categorical_columns = ['status_rumah_tinggal', 'status_pekerjaan', 'kondisi_rumah', 'kelurahan', 'bansos']
    
    # Impute missing values for categorical columns with most frequent value
    imputer = SimpleImputer(strategy='most_frequent')
    df[categorical_columns] = imputer.fit_transform(df[categorical_columns])
    
    # Encode categorical variables
    label_encoders = {col: LabelEncoder().fit(df[col]) for col in categorical_columns}
    for col, encoder in label_encoders.items():
        df[col] = encoder.transform(df[col])
    
    return df, label_encoders
    
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(request.url)
    
    file = request.files['file']
    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(request.url)
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        flash('File uploaded successfully', 'success')
        
        # Process uploaded CSV file
        df, label_encoders = process_csv_file(file_path)
        X = df[['jumlah_anggota', 'status_rumah_tinggal', 'status_pekerjaan', 'pendapatan_gaji', 'kondisi_rumah', 'kelurahan']]
        y = df['bansos']
        
        # Train Naive Bayes classifier (CategoricalNB for categorical features)
        model = CategoricalNB()
        model.fit(X, y)
        
        # Example prediction data
        example_data = {
            'jumlah_anggota': 4,
            'status_rumah_tinggal': 'KONTRAK',
            'status_pekerjaan': 'BURUH',
            'pendapatan_gaji': 4000000,
            'kondisi_rumah': 'SEDANG',
            'kelurahan': 'PEKAYON JAYA'
        }
        
        # Encode the example prediction data
        for col, encoder in label_encoders.items():
            if col in example_data:
                example_data[col] = encoder.transform([example_data[col]])[0]
        
        new_data = pd.DataFrame([example_data])
        
        predicted_bansos = model.predict(new_data)
        predicted_bansos_label = label_encoders['bansos'].inverse_transform(predicted_bansos)[0]
        flash(f"IWAN SETIAWAN likely qualifies for bansos: {predicted_bansos_label}", 'info')

        return render_template('assistance/assistance.html', table_data=df.to_dict('records'))
    
    return redirect(request.url)