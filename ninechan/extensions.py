import flask.ext.mongoengine as flask_mongoengine
import flask.ext.sqlalchemy as flask_sqlalchemy

__author__ = 'takeshix'
__all__ = ['db']


db = flask_mongoengine.MongoEngine()
sql = flask_sqlalchemy.SQLAlchemy()