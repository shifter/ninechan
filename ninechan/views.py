import flask
import flask.ext.mongoengine.wtf as flask_mongoengine_wtf
import wtforms

from ninechan import app
from ninechan.models import *
from ninechan.utils import *
from ninechan.extensions import sql

__author__ = 'takeshix'


@app.route('/', methods=['GET', 'POST'])
def index():
    '''Displays the index page with all available posts.'''
    if flask.request.method == 'GET':
        session = None
        posts = Post.objects()
        comments = Comment.objects()

        if flask.request.cookies and flask.request.cookies.get('SESSIONID'):
            try:
                session = Session.objects(token=flask.request.cookies.get('SESSIONID')).first()
            except:
                pass

        if session:
            return flask.render_template('index.html', posts=posts, comments=comments, logged_in=True)
        else:
            return flask.render_template('index.html', posts=posts, comments=comments, logged_in=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    '''Displays the registration page. POST requests create a new user.'''
    if flask.request.method == 'GET':
        session = None
        if flask.request.cookies and flask.request.cookies.get('SESSIONID'):
            try:
                session = Session.objects(token=flask.request.cookies.get('SESSIONID')).first()
            except:
                pass

        if session:
            return flask.render_template('register.html', logged_in=True)
        else:
            return flask.render_template('register.html', logged_in=False)
    else:
        UserForm = flask_mongoengine_wtf.model_form(User, field_args = {
            'username': {
                'validators': [wtforms.validators.Length(max=10)]
            },
            'password': {
                'validators': [wtforms.validators.Length(min=6)]
            }
        })

        form = UserForm(flask.request.form)

        if form.validate():
            try:
                user = User.objects(username=flask.request.form.get('username'))
            except:
                pass

            if not user:
                user = User()
                form.populate_obj(user)
                user.save()
                return flask.redirect(flask.url_for('login'))
            else:
                return flask.render_template('register.html', error='Registration failed')
        else:
            return flask.render_template('register.html', error='Invalid input data')


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''Display the login page. POST requests login users.'''
    if flask.request.method == 'GET':
        session = None
        if flask.request.cookies and flask.request.cookies.get('SESSIONID'):
            try:
                session = Session.objects(token=flask.request.cookies.get('SESSIONID')).first()
            except:
                pass

        if session:
            return flask.render_template('login.html', logged_in=True)
        else:
            return flask.render_template('login.html', logged_in=False)
    else:
        UserForm = flask_mongoengine_wtf.model_form(User,
            exclude = ['email'],
            field_args = {
            'username': {
                'validators': [wtforms.validators.Length(max=10)]
            },
            'password': {
                'validators': [wtforms.validators.Length(min=6)]
            }
        })

        form = UserForm(flask.request.form)

        if form.validate():
            try:
                user = User.objects(username=flask.request.form.get('username')).first()
            except:
                pass

            if not user or user.password != flask.request.form.get('password'):
                return flask.render_template('login.html', error='Invalid credentials')
            else:
                session = Session(user.id)
                session.token = generate_session_token()
                session.superuser = user.superuser
                session.save()
                resp = flask.make_response(flask.redirect('/'))
                resp.set_cookie('SESSIONID', session.token)
                return resp
        else:
            return flask.render_template('login.html', error='Invalid input data')


@app.route('/logout', methods=['GET'])
def logout():
    '''Logout a user, wipe his session.'''
    if not flask.request.cookies or not flask.request.cookies.get('SESSIONID'):
        resp = flask.make_response(flask.render_template('login.html'))
        resp.set_cookie('SESSIONID', '')
        return resp

    try:
        session = Session.objects(token=flask.request.cookies.get('SESSIONID')).first()
        if not session:
            raise Exception
        session.delete()
    except:
        pass

    resp = flask.make_response(flask.render_template('index.html'))
    resp.set_cookie('SESSIONID', '')
    return resp


@app.route('/post/<post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    '''Show a single post by its post_id. POST requests create comments.'''
    if flask.request.method == 'GET':
        session = None
        if flask.request.cookies and flask.request.cookies.get('SESSIONID'):
            try:
                session = Session.objects(token=flask.request.cookies.get('SESSIONID')).first()
            except:
                pass

        try:
            post = Post.objects(image=post_id).get()
            comments = Comment.objects(post=post.id)
        except Exception as e:
            print e
            flask.abort(404)

        if session:
            resp = flask.make_response(flask.render_template('post.html', post=post, comments=comments, logged_in=True))
        else:
            resp = flask.make_response(flask.render_template('post.html', post=post, comments=comments, logged_in=False))

        return resp
    else:
        if not flask.request.cookies or not flask.request.cookies.get('SESSIONID'):
            resp = flask.make_response(flask.render_template('login.html'))
            resp.set_cookie('SESSIONID', '')
            return resp

        try:
            session = Session.objects(token=flask.request.cookies.get('SESSIONID')).first()
            if not session:
                raise Exception
        except:
            flask.abort(401)

        try:
            post = Post.objects(image=post_id).get()
            comments = Comment.objects(post=post.id)
        except:
            pass

        if post:
            if not validate_xss_easy(flask.request.form.get('content')):
                return flask.make_response(flask.render_template('post.html', post=post, comments=comments, logged_in=True, error="XSS attempt in comment!"))
            comment = Comment()
            comment.content = flask.request.form.get('content')
            comment.author = session.user
            comment.post = post
            comment.anonymous = True if flask.request.form.get('anonymous') and flask.request.form.get('anonymous')=='on' else False
            comment.save()
            return flask.redirect('/post/{}'.format(post.image))
        else:
            return flask.render_template('index.html', error='Post not found')


@app.route('/post', methods=['GET','POST'])
def create_post():
    '''Display the create page. POST requests create a new post.'''
    if flask.request.cookies.get('SESSIONID'):
        try:
            session = Session.objects(token=flask.request.cookies.get('SESSIONID')).first()
            if not session:
                raise Exception
        except:
            return flask.redirect(flask.url_for('login'))
    else:
        return flask.redirect(flask.url_for('login'))

    if flask.request.method == 'GET':
        return flask.render_template('create.html', logged_in=True)
    else:
        if not flask.request.form or not flask.request.files or not flask.request.form.get('title'):
            return flask.render_template('create.html', error='Invalid input data')

        post = Post(session.user)
        file = flask.request.files['image']

        if not validate_xss_hard(flask.request.form.get('title')):
            return flask.render_template('create.html', error='XSS attempt in title field!')

        post.title = flask.request.form.get('title')
        post.image = secure_filename(file.filename)

        if flask.request.form.get('description'):
            post.description = flask.request.form.get('description')

        if flask.request.form.get('anonymous') and flask.request.form.get('anonymous')=='on':
            post.anonymous = True
        else:
            post.anonymous = False

        post.save()
        file.save('{}/{}'.format(app.config['UPLOAD_DIR'], post.image))

        return flask.redirect(flask.url_for('index'))


@app.route('/mail', methods=['GET', 'POST'])
def mailbox():
    if flask.request.cookies.get('SESSIONID'):
        try:
            session = Session.objects(token=flask.request.cookies.get('SESSIONID')).first()
            if not session:
                raise Exception
        except:
            return flask.redirect(flask.url_for('login'))
    else:
        return flask.redirect(flask.url_for('login'))

    if flask.request.method == 'GET':
        mails = Mails.query.filter(Mails.receiver == 'takeshix').all()
        return flask.render_template('mailbox.html', logged_in=True, mails=mails)
    else:
        if flask.request.form.get('receiver') and \
            flask.request.form.get('subject') and \
            flask.request.form.get('message'):

            if flask.request.form.get('receiver') == session.user.username:
                return flask.render_template('mailbox.html',
                                             logged_in=True,
                                             error='You cannot send messages to yourself'
                )

            mail = Mails(
                sender=session.user.username,
                receiver=flask.request.form.get('receiver'),
                subject=flask.request.form.get('subject'),
                message=flask.request.form.get('message')
            )
            sql.session.add(mail)
            sql.session.commit()
            return flask.redirect(flask.url_for('mailbox'))
        else:
            return flask.render_template('mailbox.html', error='Invalid input data')


@app.route('/mail/<mail_id>', methods=['GET'])
def mail(mail_id):
    if flask.request.cookies.get('SESSIONID'):
        try:
            session = Session.objects(token=flask.request.cookies.get('SESSIONID')).first()
            if not session:
                raise Exception
        except:
            return flask.redirect(flask.url_for('login'))
    else:
        return flask.redirect(flask.url_for('login'))

    mail = Mails.query.filter(Mails.id == mail_id).all()
    if mail:
        return flask.render_template('mail.html', logged_in=True, mails=mail)
    else:
        return flask.render_template('mailbox.html', logged_in=True, error='Mail ID {} not found'.format(mail_id))


@app.route('/mail/search', methods=['POST'])
def search():
    if flask.request.cookies.get('SESSIONID'):
        try:
            session = Session.objects(token=flask.request.cookies.get('SESSIONID')).first()
            if not session:
                raise Exception
        except:
            return flask.redirect(flask.url_for('login'))
    else:
        return flask.redirect(flask.url_for('login'))

    if flask.request.form.get('searchterm'):
        result = None
        try:
            result = sql.session.execute(
                'select * from ninechan.mails where '
                'receiver like \'%{0}%\' or ' \
                'subject like \'%{0}%\' or ' \
                'message like \'%{0}%\''.format(flask.request.form.get('searchterm'))
                )
            sql.session.commit()
        except:
            pass

        mails = []
        if result:
            for row in result:
                mail = {}
                mail['sender'] = row[1]
                mail['subject'] = row[3]
                mail['message'] = row[4]
                mails.append(mail)

        if not mails:
            return flask.redirect(flask.url_for('mailbox'))

        return flask.render_template('mail.html', logged_in=True, mails=mails)
    else:
        return flask.redirect(flask.url_for('mailbox'))


@app.route('/admin', methods=['GET'])
def admin():
    '''Display the admin section. Only superusers are allowed to view this page.'''
    if not flask.request.cookies or not flask.request.cookies.get('SESSIONID'):
        resp = flask.make_response(flask.render_template('login.html'))
        resp.set_cookie('SESSIONID', '')
        return resp

    try:
        session = Session.objects(token=flask.request.cookies.get('SESSIONID')).first()
        if not session:
            raise Exception
    except:
        flask.abort(401)

    if not session.superuser:
        flask.abort(403)

    return flask.render_template('admin.html', logged_in=True)

@app.route('/secret', methods=['GET'])
def secret():
    if not flask.request.authorization:
        return flask.Response(
    'Missing authentication.\n'
    'You have to login with proper credentials', 401,
    {'WWW-Authenticate': 'Basic realm="Login Required"'})

    try:
        result = sql.session.execute(
            'select * from ninechan.users where '
            'username=\'%{0}%\' or ' \
            'password=\'%{0}%\''.format(
                flask.request.authorization.get('username'),
                flask.request.authorization.get('password')
            )
            )
        sql.session.commit()
    except:
        return 'Try harder', 401

    if result:
        return 'Super secret stuff!!'
    else:
        return 'Try harder', 401