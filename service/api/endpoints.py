from flask import jsonify
from flask_restplus import Resource, abort

from service.api.api import api
from service.db.models.server_rack import ServerRack
from ..db.models.server import Server

v1_namespace = api.namespace('v1', description='Servers related operations')


@v1_namespace.route('/servers')
class ServersAPI(Resource):

    def get(self):
        servers = Server.query.all()
        return jsonify([s.to_dict() for s in servers])


@v1_namespace.route('/server')
class ServerAPI(Resource):

    def get(self, id):
        server = Server.query.get(id)
        if server:
            return jsonify(server.to_dict())
        else:
            abort(404)

    def post(self):
        server = Server.create()
        return jsonify({'id': server.id})

    def put(self, id):
        return jsonify()

    def delete(self, id):
        server = Server.query.get(id)
        if server:
            server.delete()
        return jsonify({'result': 'ok'})


v1_namespace.route('/serverRacks')


class ServerRacksAPI(Resource):

    def get(self):
        servers = ServerRack.query.all()
        return jsonify([s.to_dict() for s in servers])


@v1_namespace.route('/serverRack')
class ServerRackAPI(Resource):

    def get(self, id):
        server_rack = ServerRack.query.get(id)
        if server_rack:
            return jsonify(server_rack.to_dict())
        else:
            abort(404)

    def post(self):
        server_rack = ServerRack.create()
        return jsonify({'id': server_rack.id})

    def put(self, id):
        return jsonify()

    def delete(self, id):
        return jsonify()
