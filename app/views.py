from app import app,db
import flask
from app.models import User,comment
import hashlib

# from models import User, Post, ROLE_USER, ROLE_ADMIN email

@app.route('/index/<username>', methods=['GET','post'])#博客主页
def index(username):
    user = db.session.query(User).filter(User.db_username==username).one()
    return flask.render_template('blog_index.html', name=username, user=user)

@app.route('/gallery/<username>', methods=['GET','post'])#留言
def gallery(username):
    user = db.session.query(User).filter(User.db_username==username).one()
    if flask.request.method == 'POST':
        title = flask.request.form['title']
        text = flask.request.form['text']       
        t = comment(db_username=username, db_title=title, db_comments=text)
        db.session.add(t)
        db.session.commit()
        return flask.redirect(flask.url_for('gallery',username=username, user=user))

    elif flask.request.method == 'GET':
        comments = db.session.query(comment).all()

        return flask.render_template('blog_gallery.html', name=username, comments=comments, user=user)

# User(db_username=username, db_passworld=str(pd_md5))
@app.route('/contact/<username>', methods=['GET','post'])#个人信息
def contact(username):
    if flask.request.method == 'POST':
        user = db.session.query(User).filter(User.db_username==username).one()
        email = flask.request.form['email']
        phone = flask.request.form['phone']
        intro = flask.request.form['text']
        # intro = flask.request.form['text']
        user.db_email = email
        user.db_phone = phone
        user.db_intro = intro
        # user.db_intro = intro
        db.session.commit()       
        return flask.render_template('blog_contact.html', name=username,user=user)

    elif flask.request.method == 'GET':
        user = db.session.query(User).filter(User.db_username==username).one()
        return flask.render_template('blog_contact.html', name=username, user=user)

@app.route('/', methods=['get'])
def hello():
    return flask.redirect(flask.url_for('signin'))


@app.route('/signin', methods=['GET','post'])#用户登录
def signin():
    if flask.request.method == 'GET':
        return flask.render_template('signin.html')

    elif flask.request.method == 'POST':
        username = flask.request.form['username']
        password = flask.request.form['password']

        try:
            user = db.session.query(User).filter(User.db_username==username).one()
        except :
            return flask.redirect(flask.url_for('error', Error='用户未注册'))
        
        pd_temp = hashlib.md5(password.encode("utf-8"))
        pd_md5 = pd_temp.hexdigest()#md5加密

        if user.db_passworld == pd_md5 :
            return flask.redirect(flask.url_for('index',username=username))
        else: 
            return flask.redirect(flask.url_for('error', Error='密码错误'))

@app.route('/error/<Error>')
def error(Error):
    return flask.render_template('error.html', Error=Error)


@app.route('/signup', methods=['GET','post'])#用户注册
def signup():
    if flask.request.method == 'GET':
        return flask.render_template('index_signup.html')
    elif flask.request.method == 'POST':
        
        username = flask.request.form['name']
        try:
            db.session.query(User).filter(User.db_username==username).one()
            return flask.redirect(flask.url_for('error', Error='用户已存在'))
        except:
            pass

        Password = flask.request.form['password']
        confirm_password = flask.request.form['confirm_password']
        if confirm_password != Password :
            return flask.redirect(flask.url_for('error', Error='两次密码不一致'))

        pd_temp = hashlib.md5(Password.encode("utf-8"))#密码加密
        pd_md5 = pd_temp.hexdigest()
        u = User(db_username=username, db_passworld=str(pd_md5))
        try:
            db.session.add(u)
            db.session.commit()
            return flask.redirect(flask.url_for('index',username=username))
        except :
            return 'something go wrong'



# @app.route('/set_cookie')
# def set_cookie():
#     response = flask.make_response('Hello World')
#     response.set_cookie('Name','Hyman')
#     return response

# @app.route('/get_cookie')
# def get_cookie():
#     name = flask.request.cookies.get('Name')
#     return name

@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template('index_404.html'), 404