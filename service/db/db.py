import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')

db_engine = create_engine(SQLALCHEMY_DATABASE_URI)
db_sqlalchemy = SQLAlchemy()


