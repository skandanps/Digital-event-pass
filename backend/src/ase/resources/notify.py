import threading
from datetime import datetime, timedelta
import time
import pytz


from sqlalchemy import and_

from src.ase.db_models.Events import Event
from src.ase.db_models.user_events import UserEvent
from src.ase.message_broker.producer import send_message_to_broker
from src.ase import db


def notify_users(app):
    with app.app_context():
        print("asdawds")
        interval = 5 *10  # 5 minutes in seconds
        timer = threading.Timer(interval, notify_users, args=(app,))
        timer.daemon = True
        timer.start()

        print("Background task running...")
        current_time = datetime.now(tz=pytz.timezone('US/Central'))
        time_limit = current_time + timedelta(minutes=30)

        user_ids = [ue.user_id for ue in UserEvent.query.filter(
            and_(UserEvent.event_time > current_time, UserEvent.event_time <= time_limit)).all()]

        # create dictionary with user_id as key and list of event_ids as value
        user_event_dict = {}
        for user_id in user_ids:
            event_ids = [ue.event_id for ue in UserEvent.query.filter_by(user_id=user_id, notified=False).all()]
            user_event_dict[user_id] = event_ids

            # make a function call to send message for each user and event id
            for event_id in event_ids:
                event = Event.query.filter_by(id=event_id).first()
                event_name = event.name

                send_message_to_broker(str(user_id), str(user_id), str(event_name) + " starting sooon..")
                user_event = UserEvent.query.filter_by(user_id=user_id,event_id=event_id,notified=False).first()


                # Update the notified field to True
                user_event.notified = True

                # Commit the changes to the database
                db.session.commit()
        # Call your function to send message to broker here
        print(user_ids)
        time.sleep(10) # Sleep for 15 minutes
