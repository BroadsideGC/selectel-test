from __future__ import annotations

import logging
import random
from datetime import datetime
from enum import auto, IntEnum
from time import sleep
from typing import List

from sqlalchemy import desc

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

    @classmethod
    def get_all(cls, sort_by_date: bool, include_deleted: bool) -> List[Server]:
        if sort_by_date:
            sort_by = desc(Server.date_modified)
        else:
            sort_by = Server.id

        if include_deleted:
            servers = Server.query.order_by(sort_by).all()
        else:
            servers = Server.query.order_by(sort_by).filter(Server.status != ServerStatus.DELETED)
        return servers

    def action_pay(self, expiration_date: int) -> None:
        if self.status == ServerStatus.UNPAID:
            self.status = ServerStatus.PAID

        self.date_expiration = datetime.fromtimestamp(expiration_date)
        db_sqlalchemy.session.commit()
        logging.info('Server with id {} paid'.format(self.id))

        if self.status != ServerStatus.ACTIVE:
            sleep(random.randint(5, 7))
            self.activate()

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
