from flask import render_template, session, redirect, url_for, current_app
from . import main
from .forms import NameForm
from .. import db
from ..common.email import send_email
from apps.models import User


@main.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            if current_app.config['FLASKY_ADMIN']:
                send_email(current_app.config['FLASKY_ADMIN'], 'New User',
                           'mail/new_user', user=user)
        else:
            session['known'] = True
        session['name'] = form.name.data
        # 同一蓝本中 的重定向可以使用简写形式，
        # 但跨蓝本的重定向必须使用带有蓝本名的完全限定端点名
        # main.index
        return redirect(url_for('.index'))
    return render_template('index.html',
                           form=form, name=session.get('name'),
                           known=session.get('known', False))
