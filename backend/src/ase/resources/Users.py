from flask import request
from flask_restful import Resource
from werkzeug.security import check_password_hash

from src.ase.db_models.Users import User, UserSchema
from src.ase import db

class CreateUser(Resource):
    def post(self):
        data = request.get_json()
        new_user = User(username=data['username'],
                        password=data['password'],
                        phone_number=data['phone_number'],
                        email=data['email'],
                        address=data['address'],
                        barcode='DUMMY')
        new_user.password = data['password']
        try:
            db.session.add(new_user)
            db.session.commit()
            barcode = f"BAR{new_user.id:06}"
            new_user.barcode = barcode
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return {"error": "err-creating-user: Duplicate phone number or email address."}, 500
        return {'message': 'User created successfully'}, 201

    def get(self):
        username = request.args.get('username')
        password = request.args.get('password')

        if username != None and password != None:
            user = User.query.filter_by(username=username).first()
            if not user:
                return {'error': 'Invalid username or password'}, 401
            if not check_password_hash(user.password_hash, password):
                return {'error': 'Invalid username or password'}, 401
            # return {'message': 'User authenticated successfully'}, 200
            user_schema = UserSchema()
            return user_schema.dump(user), 200
        else:
            user = User.query.all()
            if not user:
                return {'error': 'Invalid username or password'}, 401
            if not check_password_hash(user.password_hash, password):
                return {'error': 'Invalid username or password'}, 401
            # return {'message': 'User authenticated successfully'}, 200
            user_schema = UserSchema()
            return user_schema.dump(user), 200

    def put(self):

        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if not user:
            return {'message': 'User not found'}, 404
        user.username = data['username']
        user.password = data['password']
        user.phone_number = data['phone_number']
        user.email = data['email']
        user.address = data['address']
        db.session.commit()
        return {'message': 'User updated successfully'}, 200

    def delete(self):
        data = request.get_json()
        username = data['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User not found'}, 404
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200