from datetime import datetime

import pytz

from src.ase import db
from src.ase import ma


class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(250), nullable=True)
    created_on = db.Column(db.DateTime, default=datetime.now( tz=pytz.timezone('US/Central')))
    last_updated_on = db.Column(db.DateTime, default=datetime.now( tz=pytz.timezone('US/Central')), onupdate=datetime.now(tz=pytz.timezone('US/Central')))



class DepartmentSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "description", "created_on", "last_updated_on")


department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)

