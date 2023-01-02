import logging
import sys
import traceback

from flask import Flask, jsonify
from werkzeug.debug import DebuggedApplication

from web.deploy import demo_bp
from web.deploy.gunicore_app import GunicornApp

app = Flask(__name__)


def setup():
    # scheduler.init_app(app)
    # scheduler.start()
    app.register_blueprint(demo_bp.bp)


@app.before_request
def check_auth():
    ...


@app.errorhandler(404)
def handle_404_error(err_msg):
    return jsonify(code=404, message=str(err_msg))


@app.errorhandler(Exception)
def handle_exception(e):
    logging.error('internal error :{}'.format(traceback.format_exc()))
    return jsonify(code=500, message='internal error.')


if __name__ == '__main__':
    setup()
    port = 10000

    options = {
        'bind': '%s:%s' % ('0.0.0.0', port),
        'timeout': 0,  # 600 值为正数或 0。将其设置为 0 会通过完全禁用所有 worker 的超时来实现无限超时
        'workers': 2,
    }
    GunicornApp(DebuggedApplication(app, evalex=False), options).run()
