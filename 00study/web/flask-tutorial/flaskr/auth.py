import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


# @bp.route将 URL /register 与register视图函数相关联。
# 当 Flask 收到对/auth/register的请求时，它会调用register视图并使用返回值作为响应。
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO todo (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                # 为了安全起见，永远不要将密码直接存储在数据库中。
                # 相反， generate_password_hash()用于安全地散列密码，并存储该散列。
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                # url_for()根据名称生成登录视图的 URL
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM todo WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# bp.before_app_request()注册一个在视图函数之前运行的函数，
# 无论请求什么 URL。load_logged_in_user检查用户 ID 是否存储在session
# 并从数据库中获取该用户的数据
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM todo WHERE id = ?', (user_id,)
        ).fetchone()


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


# 在其他视图中需要身份验证
# 装饰器可用于检查它应用到的每个视图
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
