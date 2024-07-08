from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'pengguna'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    nama_lengkap = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.nama_lengkap}')"

class Citizen(db.Model):
    __tablename__ = 'citizen'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(255), nullable=False)
    alamat = db.Column(db.String(255), nullable=False)
    pendapatan = db.Column(db.BigInteger, nullable=False)
    status_rumah_tinggal = db.Column(db.String(255), nullable=False)
    status_pekerjaan = db.Column(db.String(255), nullable=False)
    kondisi_rumah = db.Column(db.String(255), nullable=False)
    jumlah_anggota_keluarga = db.Column(db.String(255), nullable=False)
    status_bantuan = db.Column(db.String(255), nullable=False)
    informasi_tambahan = db.Column(db.Text, nullable=True)