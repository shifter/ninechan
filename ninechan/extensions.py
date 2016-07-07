import flask_mongoengine
import flask_sqlalchemy

__author__ = 'takeshix'
__all__ = ['db', 'sql']

db = flask_mongoengine.MongoEngine()
sql = flask_sqlalchemy.SQLAlchemy()
