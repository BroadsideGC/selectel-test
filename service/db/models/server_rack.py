from typing import List

from service.db.db import db_sqlalchemy
from service.db.models.base import Base
from service.db.models.server import Server


class ServerRack(Base):
    __tablename__ = 'serverrack'

    size = db_sqlalchemy.Column(db_sqlalchemy.Integer)

    def __init__(self, size):
        self.servers = self.__load_servers()
        self.size = size

    def __load_servers(self) -> List[Server]:
        result = Server.query.filter(Server.server_rack_id == self.id).all()
        return list(result)

    @classmethod
    def create(self, is_big=False):
        size = 20 if is_big else 10
        server_rack = ServerRack(size)
        db_sqlalchemy.session.add(server_rack)
        db_sqlalchemy.session.commit()
        return server_rack

    def to_dict(self):
        result = {
            'id': self.id,
            'size': self.size,
            'created': self.date_created,
            'modified': self.date_modified,
            'servers': [s.to_dict() for s in self.servers]
        }

        return result
