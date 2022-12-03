from flask_pagedown import PageDown

from config import config
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager

# Bootstrap 是客户端框架
bootstrap = Bootstrap()
# 使用Flask-Moment本地化日期和时间
moment = Moment()
# 关系型数据库框架
db = SQLAlchemy()
pagedown = PageDown()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    # 添加路由和自定义的错误页面
    from apps.todo import todo_bp
    app.register_blueprint(todo_bp)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    # TODO:...
    # print(app.url_map)
    # app.app_context().push()
    # print(current_app.name)
    return app
