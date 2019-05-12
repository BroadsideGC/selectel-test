from __future__ import annotations

import time
from enum import auto, IntEnum, Enum

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


class Server(db_sqlalchemy.Model):
    id = db_sqlalchemy.Column(db_sqlalchemy.Integer, primary_key=True)
    status = db_sqlalchemy.Column(db_sqlalchemy.Text)
    creation_ts = db_sqlalchemy.Column(db_sqlalchemy.TIMESTAMP)
    modification_ts = db_sqlalchemy.Column(db_sqlalchemy.TIMESTAMP)

    def __init__(self):
        self.creation_ts = time.time()
        self.modification_ts = time.time()
        self.status = Server.ServerStatus.UNPAID
