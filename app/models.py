from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin, db.Model):
    __bind_key__ = 'budget_db'
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key= True)
    username = db.Column(db.String(20), unique= True, nullable= False)
    email = db.Column(db.String(120), unique= True, nullable= False)
    phone_number = db.Column(db.String(20), unique= True, nullable= False)
    password_hash =db.Column(db.String(128), nullable= False)
    family_code = db.Column(db.String(6), unique= True)
    is_admin = db.Column(db.Boolean, default= False)
    email_verified =  db.Column(db.Boolean, default= False)
    phone_verified =  db.Column(db.Boolean, default= False)
    created_at = db.Column(db.DateTime, default= datetime.utcnow)

    db.relationship('OTP', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash= generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}) #passing the payload to the serializer object

    @staticmethod #telling python that we are not using self to fetch the values 
    def verify_reset_token(token, expiration=3600):
        user_id = None
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token,max_age=expiration)['user_id']
        except:
            None
        return User.query.get(user_id)

class OTP(db.Model):
    __bind_key__ = 'budget_db'
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key= True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable= False)
    otp_type = db.Column(db.String(20), nullable = False)
    otp_value = db.Column(db.String(6),nullable =False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)
    expires_at = db.Column(db.DateTime, default = datetime.utcnow)
    is_used = db.Column(db.Boolean, default= False)

    def __init__(self, user_id, otp_type, otp_value, expiry_minutes = 10):
        self.user_id = user_id
        self.otp_type = otp_type
        self.otp_value = otp_value
        self.created_at = datetime.utcnow()
        self.expires_at = self.created_at + timedelta(minutes=expiry_minutes)

    def is_valid(self):
        return not self.is_used and datetime.utcnow() <= self.expires_at
    
    def use(self):
        self.is_used = True
        db.session.commit()


