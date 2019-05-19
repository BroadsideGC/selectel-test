from flask import jsonify, request
from flask_restplus import Resource, reqparse

from service.api.api import api, RESULT_OK
from service.db.models.server_rack import ServerRack
from ..db.models.server import Server, ServerStatus

v1_namespace = api.namespace('v1', description='Servers related operations')

sort_by_date_reqparser = reqparse.RequestParser()
sort_by_date_reqparser.add_argument('sortByDate', type=bool, default=False)
action_reqparser = reqparse.RequestParser()
action_reqparser.add_argument('action', type=str, required=True, location=['json'])
expiration_date_reqparser = reqparse.RequestParser()
expiration_date_reqparser.add_argument('expirationDate', type=int, required=True, location=['json'])
is_big_reqparser = reqparse.RequestParser()
is_big_reqparser.add_argument('isBig', type=bool, default=False)
server_id_reqparser = reqparse.RequestParser()
server_id_reqparser.add_argument('serverId', type=int, required=True, location=['json'])


@v1_namespace.route('/servers')
class ServersAPI(Resource):

    def get(self):
        sort_by_date = sort_by_date_reqparser.parse_args(request).get('sortByDate')
        if sort_by_date:
            sort_by = Server.date_created
        else:
            sort_by = Server.id
        servers = Server.query.order_by(sort_by).all()
        return jsonify([s.to_dict() for s in servers])

    def post(self):
        server = Server.create()
        return jsonify({'result': {'id': server.id}})


@v1_namespace.route('/servers/<int:id>')
class ServerAPI(Resource):

    def get(self, id):
        server = Server.query.get(id)
        if server:
            if server.status == ServerStatus.DELETED:
                v1_namespace.abort(410, 'Server deleted')
            return jsonify(server.to_dict())
        else:
            v1_namespace.abort(404, 'Server not found')

    def put(self, id):
        server = Server.query.get(id)
        if server:
            if server.status == ServerStatus.DELETED:
                v1_namespace.abort(410, 'Server deleted')
            action = action_reqparser.parse_args(request).get('action')
            if action == 'pay':
                expiration_date = expiration_date_reqparser.parse_args(request).get('expirationDate')
                server.action_pay(expiration_date)
            else:
                return v1_namespace.abort(400, 'Invalid action with server')
            return jsonify(RESULT_OK)
        else:
            v1_namespace.abort(404, 'Server not found')

    def delete(self, id):
        server = Server.query.get(id)
        if server:
            server.delete()
        return jsonify(RESULT_OK)


@v1_namespace.route('/serverRacks')
class ServerRacksAPI(Resource):

    def get(self):
        sort_by_date = sort_by_date_reqparser.parse_args(request).get('sortByDate')
        if sort_by_date:
            sort_by = ServerRack.date_created
        else:
            sort_by = ServerRack.id
        server_rack = ServerRack.query.order_by(sort_by).all()
        return jsonify([s.to_dict() for s in server_rack])

    def post(self):
        is_big = sort_by_date_reqparser.parse_args(request).get('isBig')
        server_rack = ServerRack.create(is_big=is_big)
        return jsonify({'result': {'id': server_rack.id}})


@v1_namespace.route('/serverRacks/<int:id>')
class ServerRackAPI(Resource):

    def get(self, id):
        server_rack = ServerRack.query.get(id)
        if server_rack:
            if server_rack.deleted:
                return v1_namespace.abort(410, 'Server rack deleted')
            return jsonify(server_rack.to_dict())
        else:
            v1_namespace.abort(404, 'Server rack not found')

    def put(self, id):
        server_rack = ServerRack.query.get(id)
        if server_rack:
            if server_rack.deleted:
                v1_namespace.abort(410, 'Server rack deleted')
            action = action_reqparser.parse_args(request).get('action')
            if action == 'add-server':
                if len(server_rack.servers) == server_rack.size:
                    v1_namespace.abort(422, 'Server rack capacity already reached')
                server_id = server_id_reqparser.parse_args(request).get('serverId')
                if not server_rack.add_server(server_id):
                    v1_namespace.abort(422, 'Server belong to other server rack or doesn`t exist')
            elif action == 'remove-server':
                server_id = server_id_reqparser.parse_args(request).get('serverId')
                server_rack.add_server(server_id)
                if not server_rack.add_server(server_id):
                    v1_namespace.abort(422, 'Server doesn`t belong to server rack')
            else:
                v1_namespace.abort(400, 'Invalid action with server')
            return jsonify(RESULT_OK)
        else:
            v1_namespace.abort(404, 'Server rack not found')

    def delete(self, id):
        server_rack = ServerRack.query.get(id)
        if server_rack and not server_rack.deleted:
            server_rack.delete()
        return jsonify(RESULT_OK)
