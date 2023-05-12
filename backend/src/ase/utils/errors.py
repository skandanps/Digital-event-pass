from flask import Blueprint, jsonify

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(401)
def authentication_error(error):
    return jsonify(error=str(error)), 401


@errors.app_errorhandler(400)
def client_error(error):
    return jsonify(error=str(error)), 400


@errors.app_errorhandler(404)
def page_not_found(error):
    return jsonify(error=str(error)), 404


@errors.app_errorhandler(500)
def application_error(error):
    return jsonify(error=str(error)), 500
