from __future__ import annotations

import datetime
import logging
import time
from typing import List

from sqlalchemy import orm, desc

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
    def create(cls, is_big=False) -> ServerRack:
        size = 20 if is_big else 10
        server_rack = ServerRack(size)
        db_sqlalchemy.session.add(server_rack)
        db_sqlalchemy.session.commit()
        logging.info('Server rack created with id {}'.format(server_rack.id))
        return server_rack

    @classmethod
    def get_all(cls, sort_by_date: bool, include_deleted: bool) -> List[ServerRack]:
        if sort_by_date:
            sort_by = desc(ServerRack.date_modified)
        else:
            sort_by = ServerRack.id

        if include_deleted:
            server_rack = ServerRack.query.order_by(sort_by).all()
        else:
            server_rack = ServerRack.query.order_by(sort_by).filter(ServerRack.deleted == False)
        return server_rack

    def add_server(self, server_id: int) -> bool:
        server = Server.query.get(server_id)
        if not server:
            logging.error('Trying to add non existing server to rack with id {}'.format(server_id))
            return False
        if not server.server_rack_id:
            server.server_rack_id = self.id
            self.date_modified = datetime.datetime.fromtimestamp(time.time())
            db_sqlalchemy.session.commit()
            self.servers = self.__load_servers()
            logging.info('Server with id {} added to rack with id {}'.format(server_id, self.id))
            return True
        elif server.server_rack_id == self.id:
            logging.info('Server with id {} already in rack with id {}'.format(server_id, self.id))
            return True
        else:
            logging.error(
                'Server with id {} can`t be added to rack with id {}, because already in rack with id'.format(server_id,
                                                                                                              self.id,
                                                                                                              server.server_rack_id))
            return False

    def remove_server(self, server_id: int) -> bool:
        server = Server.query.get(server_id)
        if server:
            if server.server_rack_id == self.id:
                server.server_rack_id = None
                self.date_modified = datetime.datetime.fromtimestamp(time.time())
                db_sqlalchemy.session.commit()
                self.servers = self.__load_servers()
                logging.info('Server with id {} removed from rack with id {}'.format(server_id, self.id))
                return True
            else:
                logging.error(
                    'Server with id {} can`t be removed from rack with id {} because belong to rack with id {}'.format(
                        server_id, self.id, server.server_rack_id))
                return False
        else:
            logging.error('Trying to remove non existing server by id {}'.format(server_id))
            return False

    def delete(self) -> None:
        for server in self.servers:
            server.server_rack_id = None
        self.deleted = True
        db_sqlalchemy.session.commit()
        self.servers = []
        logging.info('Server rack with id {} deleted'.format(self.id))

    def to_dict(self):
        result = {
            'id': self.id,
            'size': self.size,
            'created': self.date_created,
            'modified': self.date_modified,
            'servers': [s.to_dict() for s in self.servers],
            'isDeleted': self.deleted
        }

        return result
