import json
from datetime import datetime

import pytz
from flask import jsonify, Response
from flask_restful import Resource, Api, reqparse
from marshmallow import ValidationError

from src.ase.db_models.Events import Event, EventSchema
from src.ase import db

event_schema = EventSchema()


class EventListResource(Resource):
    def get(self):
        current_time = datetime.now( tz=pytz.timezone('US/Central'))
        events = Event.query.filter(Event.date > current_time).all()
        event_schema = EventSchema(many=True)
        result = event_schema.dump(events)
        return jsonify(result)

    def post(self):
        event_schema = EventSchema()
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True, help='Name is required')
        parser.add_argument('venue', type=str, required=True, help='Venue is required')
        parser.add_argument('date', type=str, required=True, help='Date is required')
        parser.add_argument('description', type=str)
        parser.add_argument('image_url', type=str)
        args = parser.parse_args()
        event_date = datetime.strptime(args['date'], '%Y-%m-%d %H:%M:%S')
        us_central_tz = pytz.timezone('US/Central')
        event_date = us_central_tz.localize(event_date)

        if Event.query.filter_by(name=args['name']).first():
            error_msg = {'error': 'err-name-already-exists'}
            return Response(json.dumps(error_msg), status=400, content_type='application/json')

        event = Event(name=args['name'], venue=args['venue'], date=event_date,
                      description=args['description'], image_url=args['image_url'])
        db.session.add(event)
        db.session.commit()
        try:
            serialized_event = event_schema.dump(event)
        except ValidationError as e:
            return jsonify({'error': e.messages}), 400

        return serialized_event, 201


class EventResource(Resource):
    def get(self, id):
        if id is not None:
            event = Event.query.get_or_404(id)
            return {'id': event.id, 'name': event.name, 'venue': event.venue, 'date': event.date,
                    'description': event.description, 'image_url': event.image_url}
        else:
            events = Event.query.filter(Event.date >= datetime.utcnow()).all()
            event_schema = EventSchema(many=True)
            result = event_schema.dump(events)
            return jsonify(result)

    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('venue', type=str)
        parser.add_argument('date', type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('image_url', type=str)

        args = parser.parse_args()
        event = Event.query.get_or_404(id)
        if args['name']:
            event.name = args['name']
        if args['venue']:
            event.venue = args['venue']
        if args['date']:
            event.date = datetime.strptime(args['date'], '%Y-%m-%d %H:%M:%S')
        if args['description']:
            event.description = args['description']
        if args['image_url']:
            event.image_url = args['image_url']

        db.session.commit()
        return {'id': event.id, 'name': event.name, 'venue': event.venue, 'date': event.date,
                'description': event.description, 'image_url': event.image_url}

    def delete(self, id):
        event = Event.query.get_or_404(id)
        db.session.delete(event)
        db.session.commit()
        return '', 204
