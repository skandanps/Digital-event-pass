import logging

from flask_restful import Resource

log = logging.getLogger(__name__)

class Health(Resource):
    @classmethod
    def get(cls):
        log.debug("I'm alive")
        return "I'm alive", 200

