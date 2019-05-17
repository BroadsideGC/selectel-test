from __future__ import annotations

from typing import List

from sqlalchemy import orm

from service.db.db import db_sqlalchemy
from service.db.models.base import Base
from service.db.models.server import Server


class ServerRack(Base):
    __tablename__ = 'serverrack'

    size = db_sqlalchemy.Column(db_sqlalchemy.Integer)
    deleted = db_sqlalchemy.Column(db_sqlalchemy.Boolean, default=False)

    def __init__(self, size):
        self.servers = []
        self.size = size

    def __load_servers(self) -> List[Server]:
        result = Server.query.filter(Server.server_rack_id == self.id).all()
        return list(result)

    @orm.reconstructor
    def init_on_load(self):
        self.servers = self.__load_servers()

    @classmethod
    def create(self, is_big=False) -> ServerRack:
        size = 20 if is_big else 10
        server_rack = ServerRack(size)
        db_sqlalchemy.session.add(server_rack)
        db_sqlalchemy.session.commit()
        return server_rack

    def add_server(self, server_id: int) -> bool:
        server = Server.query.get(server_id)
        if not server.server_rack_id:
            server.server_rack_id = self.id
            db_sqlalchemy.session.commit()
            self.servers = self.__load_servers()
            return True
        elif server.server_rack_id == self.id:
            return True
        else:
            return False

    def delete_server(self, server_id: int) -> bool:
        server = Server.query.get(server_id)
        if server.id == server_id:
            server.server_rack_id = None
            db_sqlalchemy.session.commit()
            self.servers = self.__load_servers()
            return True
        else:
            return False

    def delete(self) -> None:
        for server in self.servers:
            server.server_rack_id = None
        self.deleted = True
        db_sqlalchemy.session.commit()
        self.servers = []

    def to_dict(self):
        result = {
            'id': self.id,
            'size': self.size,
            'created': self.date_created,
            'modified': self.date_modified,
            'servers': [s.to_dict() for s in self.servers]
        }

        return result
