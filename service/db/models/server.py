from __future__ import annotations

import logging
import random
import threading
from datetime import datetime
from enum import auto, IntEnum

from service.db.models.base import Base
from ..db import db_sqlalchemy


class ServerStatus(IntEnum):
    UNPAID = auto()
    PAID = auto()
    ACTIVE = auto()
    DELETED = auto()

    @classmethod
    def get_name(cls, status: ServerStatus) -> str:
        status_to_name = {
            ServerStatus.UNPAID: 'Unpaid',
            ServerStatus.PAID: 'Paid',
            ServerStatus.ACTIVE: 'Active',
            ServerStatus.DELETED: 'Deleted'
        }
        return status_to_name[status]

    @classmethod
    def get_next_status(cls, status: ServerStatus) -> ServerStatus:
        if status == ServerStatus.DELETED:
            return ServerStatus.DELETED
        return ServerStatus(status + 1)


class Server(Base):
    __tablename__ = 'server'

    status = db_sqlalchemy.Column(db_sqlalchemy.Integer)
    server_rack_id = db_sqlalchemy.Column(db_sqlalchemy.Integer)
    date_expiration = db_sqlalchemy.Column(db_sqlalchemy.DateTime, default=db_sqlalchemy.func.current_timestamp())

    def __init__(self):
        self.status = ServerStatus.UNPAID

    @classmethod
    def create(cls) -> Server:
        server = Server()
        db_sqlalchemy.session.add(server)
        db_sqlalchemy.session.commit()
        logging.info('Server created with id {}'.format(server.id))
        return server

    def action_pay(self, expiration_date: int) -> None:
        if self.status == ServerStatus.UNPAID:
            self.status = ServerStatus.PAID

        self.date_expiration = datetime.fromtimestamp(expiration_date)
        db_sqlalchemy.session.commit()
        logging.info('Server with id {} paid'.format(self.id))

        if self.status != ServerStatus.ACTIVE:
            thr = threading.Timer(random.randint(5, 15), self.activate)
            thr.start()

    def activate(self) -> None:
        self.status = ServerStatus.ACTIVE
        db_sqlalchemy.session.commit()
        logging.info('Server with id {} activated'.format(self.id))

    def delete(self) -> None:
        self.date_expiration = None
        self.status = ServerStatus.DELETED
        db_sqlalchemy.session.commit()
        logging.info('Server with id {} now in status deleted'.format(self.id))

    def to_dict(self) -> dict:
        result = {
            'id': self.id,
            'status': ServerStatus.get_name(self.status),
            'created': self.date_created,
            'modified': self.date_modified,
            'serverRackId': self.server_rack_id
        }
        if self.status in frozenset([ServerStatus.PAID, ServerStatus.ACTIVE]):
            result['expire'] = self.date_expiration

        return result
