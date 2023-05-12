import logging
from os import environ

log = logging.getLogger(__name__)


def load_env_vars(config):
    try:
        config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URL")
        config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        config["SQLALCHEMY_ECHO"] = False
        config["PROPAGATE_EXCEPTIONS"] = True
        config["TMP_LOC"] = environ.get("TMP_LOC", "/tmp")
        config['AUTH_PUBLIC_KEY'] = environ.get('AUTH_PUBLIC_KEY')
        config["SERVER_PORT"] = environ.get("SERVER_PORT", 9095)
        config["USE_SYSLOG"] = environ.get("USE_SYSLOG", "True")

        return config
    except Exception as e:
        log.debug(f"error while loading env variables {e}")
