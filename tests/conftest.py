import os

import pytest

from service.db.db import basedir, db_sqlalchemy


@pytest.fixture(autouse=True, scope='module')
def app():
    from service.app import create_app

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test_app.db')

    app = create_app(
        {
            'SQLALCHEMY_DATABASE_URI': SQLALCHEMY_DATABASE_URI,
        },
    )
    with app.app_context():
        yield app
        db_sqlalchemy.drop_all()


@pytest.fixture(scope='module')
def api_client(app):
    app.testing = True

    with app.test_client() as client:
        yield client
