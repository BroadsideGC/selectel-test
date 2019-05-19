import logging
import sys

from flask import Flask, Blueprint

from service.api.api import api, page_not_found
from service.api.endpoints import v1_namespace
from service.db import db
from service.settings import LOG_LEVEL


def create_app(settings=None):
    app = Flask(__name__)

    app.register_error_handler(404, page_not_found)

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

    formatter = logging.Formatter(fmt="%(asctime)s %(levelname)s %(module)s: %(message)s",
                                  datefmt="%H:%M:%S")
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(LOG_LEVEL)

    return app


if __name__ == '__main__':
    create_app()
