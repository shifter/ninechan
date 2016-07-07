import os
import flask

import ninechan.extensions
import ninechan.settings

__author__ = 'takeshix'


app = flask.Flask(__name__)

try:
    if os.environ['NINECHAN_DEV']:
        app.config.from_object(ninechan.settings.DevelopmentConfig)
except KeyError:
    app.config.from_object(ninechan.settings.BaseConfig)

ninechan.extensions.db.init_app(app)
ninechan.extensions.sql.init_app(app)

import ninechan.views