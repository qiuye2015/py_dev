import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    # __name__是当前Python模块的名称
    # instance_relative_config=True告诉应用程序配置文件是相对于实例文件夹的。
    # 实例文件夹位于flaskr包之外
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello/')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    # app.add_url_rule() 将端点名称'index'与/ url 相关联，
    # 以便 url_for('index')或url_for('blog.index')两者都可以工作，以任何一种方式生成相同的 / URL
    app.add_url_rule('/', endpoint='index')
    return app
