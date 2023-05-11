import logging
import time

from flask import Flask

from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler

scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))

# logging.getLogger('apscheduler.executors.default').setLevel(logging.WARNING)
app = Flask(__name__)  # 实例化flask
scheduler.init_app(app)  # 把任务列表放入 flask
scheduler.start()  # 启动任务列表
app.debug = True


def now():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


@app.route('/')
def hello_world():
    return 'Hello, World!'


def short_time_task():
    print(now(), "short_time_task")


def long_time_task():
    print(now(), "long_time_task")
    time.sleep(25)
    print(now(), "long_time_task end")


@scheduler.task("interval", id="cron_job", seconds=10)
def short_time_job():
    # print("starting short_time_job")
    short_time_task()
    # print("ended short_time_job")


@scheduler.task("interval", id="collect_log", seconds=25)
def long_time_job():
    # print("starting long_time_job")
    long_time_task()
    # print("ended long_time_job")


if __name__ == '__main__':
    # app.config.from_object(Config())      # 为实例化的 flask 引入配置
    # scheduler = APScheduler()                  # 实例化 APScheduler
    # scheduler.init_app(app)  # 把任务列表放入 flask
    # scheduler.start()  # 启动任务列表
    # app.debug = True
    app.run(host='0.0.0.0', port=8000)  # 启动 flask
