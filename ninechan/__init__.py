import os
import flask

import ninechan.extensions
import ninechan.settings

__author__ = 'takeshix'

app = flask.Flask(__name__)

if os.environ.get('NINECHAN_DEV'):
    app.config.from_object(ninechan.settings.DevelopmentConfig)
else:
    app.config.from_object(ninechan.settings.BaseConfig)

ninechan.extensions.db.init_app(app)
ninechan.extensions.sql.init_app(app)
import ninechan.views