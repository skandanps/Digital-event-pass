from datetime import datetime

import pytz
from flask import request
from flask_restful import Resource, reqparse
from src.ase.db_models.Events import Event, EventSchema
from src.ase import db
from src.ase.db_models.Users import UserSchema, User
from src.ase.db_models.user_events import UserEvent

user_schema = UserSchema()
event_schema = EventSchema()

parser = reqparse.RequestParser()
parser.add_argument('user_id', type=int, required=True, help='User ID is required')
parser.add_argument('event_id', type=int, required=True, help='Event ID is required')


class UserEventResource(Resource):
    def put(self):
        data = request.get_json()
        user_id = data['user_id']
        event_id = data['event_id']
        print("user and event id is",user_id,event_id)
        user = User.query.get(user_id)
        event = Event.query.get(event_id)
        if not user:
            return {'message': 'User not found'}, 404
        if not event:
            return {'message': 'Event not found'}, 404

        current_time = datetime.now( tz=pytz.timezone('US/Central'))
        event = Event.query.filter(Event.date > current_time, Event.id == event_id).first()
        if not event:
            return {"error":"event is in past / not found"}, 400

        user_event = UserEvent.query.filter_by(user_id=user_id, event_id=event_id).first()
        if user_event:
            db.session.delete(user_event)
            db.session.commit()
            return {'message': 'User cancelled event successfully'}, 200
        else:
            print("new registration..")
            new_user_event = UserEvent(user_id=user_id, event_id=event_id, event_time=event.date)
            db.session.add(new_user_event)
            db.session.commit()
            return {'message': 'User registered for event successfully'}, 200

    def get(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        user_events = UserEvent.query.filter_by(user_id=user_id).all()
        event_ids = [user_event.event_id for user_event in user_events]
        events = Event.query.filter(Event.id.in_(event_ids)).all()
        return event_schema.dump(events, many=True)


class VerifyUserRegistration(Resource):
    def get(self):
        user_id = request.args.get('user_id')
        event_id = request.args.get('event_id')
        print("user and event id is",user_id,event_id)
        user_event = UserEvent.query.filter_by(user_id=user_id, event_id=event_id).first()
        if user_event:
            return {'message': 'User registered for event successfully'}, 200
        else:
            return {'error':'user did not register for this event'}, 400
