from datetime import datetime

import pytz
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

from src.ase import db


class UserEvent(db.Model):
    __tablename__ = "user_event"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now( tz=pytz.timezone('US/Central')))
    event_time = db.Column(db.DateTime, nullable=False)
    notified = db.Column(db.Boolean, default=False)

class UserEventSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    event_id = fields.Int(required=True)
    created_at = fields.DateTime(dump_only=True)
    event_time = fields.DateTime(required=True, allow_none=False)
    notified = fields.Boolean()
