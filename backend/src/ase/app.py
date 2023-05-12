import logging
import logging.config
import logging.handlers
import threading

from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Api



from src.ase.utils.envvars import load_env_vars

API_ROOT = "/event-pass/apis"
V1_API_ROOT = "{}/v1".format(API_ROOT)
USER_API_ROOT = "{}/user".format(V1_API_ROOT)
DEPARTMENT_API_ROOT = "{}/department".format(V1_API_ROOT)
EVENTS_API_ROOT = "{}/events".format(V1_API_ROOT)

SEARCH_SUGGESTION_API_ROOT = "{}/suggestion".format(V1_API_ROOT)
app = Flask(__name__)


def create_app():
    api = Api(app)

    log = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    app.app_context().push()
    with app.app_context():
        from src.ase import ma, db
        load_env_vars(app.config)
        from src.ase.resources.Health import Health
        from src.ase.resources.Users import CreateUser
        from src.ase.resources.Events import EventListResource
        from src.ase.resources.Register import UserEventResource
        from src.ase.resources.Barcode import BarcodeResource
        from src.ase.utils.errors import errors
        from src.ase.resources.Department import DepartmentResource, DepartmentIdResource
        from src.ase.resources.Register import VerifyUserRegistration
        from src.ase.resources.notify import notify_users
        api.add_resource(DepartmentResource, '/departments')
        api.add_resource(DepartmentIdResource, '/departments/<int:department_id>')
        api.add_resource(UserEventResource,V1_API_ROOT+'/register-event/')
        api.add_resource(EventListResource,V1_API_ROOT+'/event/')
        api.add_resource(BarcodeResource, V1_API_ROOT + '/barcode/')
        api.add_resource(VerifyUserRegistration,V1_API_ROOT+"/verify/")
        ma.init_app(app)

        api.add_resource(Health, API_ROOT + "/health/")
        api.add_resource(CreateUser, USER_API_ROOT)

        app.register_blueprint(errors)
        db.init_app(app)


        # CORS(app, resources={r"/*": {"origins": ["http://localhost:8080"]}})
        log.debug("db initialised...")
        print(app.url_map)
        log.info(app.url_map)
        print("notifying")
        # notify_users(app)
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=app.config["SERVER_PORT"], debug=True)
