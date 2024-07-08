from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    nama_lengkap = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class CitizenForm(FlaskForm):
    nama = StringField('Nama', validators=[DataRequired(), Length(max=255)])
    alamat = StringField('Alamat', validators=[DataRequired(), Length(max=255)])
    pendapatan = IntegerField('Pendapatan', validators=[DataRequired()])
    status_rumah_tinggal = StringField('Status Rumah Tinggal', validators=[DataRequired(), Length(max=255)])
    status_pekerjaan = StringField('Status Pekerjaan', validators=[DataRequired(), Length(max=255)])
    kondisi_rumah = StringField('Kondisi Rumah', validators=[DataRequired(), Length(max=255)])
    jumlah_anggota_keluarga = StringField('Jumlah Anggota Keluarga', validators=[DataRequired(), Length(max=255)])
    status_bantuan = StringField('Status Bantuan', validators=[DataRequired(), Length(max=255)])
    informasi_tambahan = TextAreaField('Informasi Tambahan')
    submit = SubmitField('Submit')
