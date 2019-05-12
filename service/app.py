import logging

from flask import Flask, Blueprint

from service.api.api import api
from service.api.endpoints import v1_namespace
from service.db import db
from service.db.models.server import ServerStatus

logger = logging.getLogger(__name__)


def create_app(settings=None):
    app = Flask(__name__)

    @app.route('/')
    def hello():
        return str(ServerStatus.get_next_status(ServerStatus.UNPAID).name)

    app.config['SQLALCHEMY_DATABASE_URI'] = db.SQLALCHEMY_DATABASE_URI

    app.app_context().push()
    db.db_sqlalchemy.init_app(app)
    db.db_sqlalchemy.create_all()

    if settings:
        app.config.update(settings)

    api_bp = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(api_bp)
    api.add_namespace(v1_namespace)

    if settings:
        app.config.update(settings)

    app.register_blueprint(api_bp)

    return app


if __name__ == '__main__':
    create_app()
