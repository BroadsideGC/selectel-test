from flask import Flask
import logging

from service.db.models.server import ServerStatus
from .db import db

logger = logging.getLogger(__name__)


def create_app(settings=None):
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return str(ServerStatus.get_next_status(ServerStatus.UNPAID).name)

    app.config['SQLALCHEMY_DATABASE_URI'] = db.SQLALCHEMY_DATABASE_URI

    db.db_sqlalchemy.init_app(app)

    if settings:
        app.config.update(settings)

    return app


if __name__ == '__main__':
    create_app()
