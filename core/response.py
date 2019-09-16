
from flask import Blueprint, jsonify
errors = Blueprint('errors', __name__)

@errors.app_errorhandler(Exception)
def handle_error(error):
    message = [str(x) for x in error.args]
    success = False
    response = {
        'success': success,
        'error': {
            'type': error.__class__.__name__,
            'message': message
        }
    }

    return jsonify(response), 500