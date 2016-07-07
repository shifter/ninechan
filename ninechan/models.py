from ninechan.extensions import db, sql

__author__ = 'takeshix'
__all__ = ['User', 'Session', 'Post', 'Comment', 'Mails']


class User(db.Document):
    """Database user object"""
    username = db.StringField(required=True)
    password = db.StringField(required=True)
    superuser = db.BooleanField(
        default=False)


class Session(db.Document):
    """Database session object"""
    user = db.ReferenceField(User)
    token = db.StringField(required=True)
    superuser = db.BooleanField(
        required=True,
        default=False)


class Post(db.Document):
    """Database post object"""
    author = db.ReferenceField(User)
    anonymous = db.BooleanField(
        required=True,
        default=False)
    title = db.StringField(required=True)
    image = db.StringField(required=True)
    description = db.StringField(required=False)


class Comment(db.Document):
    """Database comment object"""
    author = db.ReferenceField(User)
    anonymous = db.BooleanField(
        required=True,
        default=False)
    post = db.ReferenceField(Post)
    content = db.StringField(required=True)


class Mails(sql.Model):
    id = sql.Column(sql.Integer, primary_key=True)
    sender = sql.Column(sql.String(50))
    receiver = sql.Column(sql.String(50))
    subject = sql.Column(sql.String(100))
    message = sql.Column(sql.String(500))
    timestamp = sql.Column(sql.DateTime, default=sql.func.now())

    def __init__(self, sender, receiver, subject, message):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.message = message

    def __repr__(self):
        return '<Mail From: {} To: {} Subject: {}'.format(self.sender, self.receiver, self.subject)