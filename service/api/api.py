import flask
from flask_restplus import Api

api = Api(version='1.0')

RESULT_OK = {'result': 'ok'}


def page_not_found(e):
    return flask.jsonify({'message': str(e)}), 404
