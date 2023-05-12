from datetime import datetime
from flask import request
from flask_restful import Resource
from src.ase import db
from src.ase.db_models.Departments import Department, DepartmentSchema

department_schema = DepartmentSchema()
departments_schema = DepartmentSchema(many=True)

class DepartmentResource(Resource):
    def post(self):
        data = request.get_json()
        department = Department(name=data['department_name'], description=data['location'])
        db.session.add(department)
        db.session.commit()
        return {'message': 'Department created successfully', 'data': department_schema.dump(department)}, 201

    def get(self):
        departments = Department.query.all()
        return {'data': departments_schema.dump(departments)}, 200

class DepartmentIdResource(Resource):
    def get(self):
        name = request.args.get("name")
        department = Department.query.filter_by(name=name).first()
        if not department:
            return {'message': 'Department not found'}, 404
        return {'data': department_schema.dump(department)}, 200

    def put(self, department_id):
        department = Department.query.get(department_id)
        if not department:
            return {'message': 'Department not found'}, 404
        data = request.get_json()
        department.name = data['name']
        db.session.commit()
        return {'message': 'Department updated successfully', 'data': department_schema.dump(department)}, 200

    def delete(self, department_id):
        department = Department.query.get(department_id)
        if not department:
            return {'message': 'Department not found'}, 404
        db.session.delete(department)
        db.session.commit()
        return {'message': 'Department deleted successfully'}, 200
