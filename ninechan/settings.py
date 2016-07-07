__author__ = 'takeshix'


class BaseConfig(object):
    WTF_CSRF_ENABLED = False
    UPLOAD_DIR = 'ninechan/static/images'
    SECRET_KEY = '\x32\xae\xfe\x8a'
    SQLALCHEMY_DATABASE_URI = ''
    MONGODB_SETTINGS = {
        'db': 'ninechan',
        'host': '127.0.0.1',
        'port': 27017}


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SECRET_KEY = '\x01\x02\x03\x04'
    SQLALCHEMY_DATABASE_URI = 'mysql://ninechan:ninechan1337@172.22.11.183/ninechan'
    MONGODB_SETTINGS = {
        'db': 'ninechan-dev',
        'host': '172.22.11.183',
        'port': 27017}