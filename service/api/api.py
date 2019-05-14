import logging

from flask_restplus import Api

log = logging.getLogger(__name__)

api = Api(version='1.0')

RESULT_OK = {'result': '0'}
RESULT_NOT_FOUND = {'error': 'not-found'}
RESULT_DELETED = {'error': 'deleted'}
RESULT_ACTION_NOT_FOUND = {'error': 'action-not-found'}


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    return {'message': message}, 500
