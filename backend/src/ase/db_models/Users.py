import pytz
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from src.ase import db
from datetime import datetime
from marshmallow import Schema, fields

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    phone_number = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(250), nullable=False)
    barcode = db.Column(db.String(50), unique=True, nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now( tz=pytz.timezone('US/Central')))
    last_updated_on = db.Column(db.DateTime, default=datetime.now( tz=pytz.timezone('US/Central')), onupdate=datetime.now(tz=pytz.timezone('US/Central')))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String(required=True)
    phone_number = fields.String(required=True)
    email = fields.Email(required=True)
    address = fields.String(required=True)
    barcode = fields.String(required=True)
    created_on = fields.DateTime(default=datetime.utcnow)
    last_updated_on = fields.DateTime(default=datetime.utcnow,
                                       missing=datetime.utcnow,
                                       dump_only=True)

