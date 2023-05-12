from datetime import datetime

import pytz
from flask_sqlalchemy import SQLAlchemy

from src.ase import db


class Event(db.Model):
    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    venue = db.Column(db.String(50), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now( tz=pytz.timezone('US/Central')))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(100))


from marshmallow import Schema, fields

class EventSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    venue = fields.Str(required=True)
    date = fields.DateTime(required=True)
    description = fields.Str()
    image_url = fields.Str()
