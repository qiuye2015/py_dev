from flask import Flask, jsonify, request, session
import logging
from logging.config import dictConfig
import uuid

# 配置是在应用程序 ( app) 初始化之前定义
dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s | %(module)s >>> %(message)s",
                "datefmt": "%B %d, %Y %H:%M:%S %Z",
            },
            "extra_user": {
                "format": "[%(asctime)s] %(levelname)s | %(module)s >>> %(message)s >>> User: %(user)s",
                "datefmt": "%B %d, %Y %H:%M:%S %Z",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            },
            "console_with_extra": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "extra_user",
            },
            "file": {
                "class": "logging.FileHandler",
                "filename": "flask.log",
                "formatter": "default",
            },
            "size-rotate": {
                "class": "logging.handlers.RotatingFileHandler",
                "filename": "flask.log",
                "maxBytes": 1000000,
                "backupCount": 5,
                "formatter": "default",
            },
            "time-rotate": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": "flask.log",
                "when": "D",
                "interval": 10,
                "backupCount": 5,
                "formatter": "default",
            },

        },
        "root": {
            "level": "DEBUG",
            "handlers": [
                # "size-rotate",
                # "time-rotate",
                "console",
                "file"
            ]
        },
        "loggers": {
            "extra": {
                "level": "INFO",
                "handlers": ["time-rotate"],
                "propagate": False,
            },
            "extra_with_extra": {
                "level": "DEBUG",
                "handlers": ["console_with_extra"],
                "propagate": False,
            }
        },
    }
)

root = logging.getLogger("root")
extra = logging.getLogger("extra")
extra_with_extra = logging.getLogger("extra_with_extra")

app = Flask(__name__)

app.secret_key = "123"


def request_parse(req_data):
    """解析请求数据并以json形式返回"""
    if req_data.method == 'POST':
        data = req_data.json
    elif req_data.method == 'GET':
        data = req_data.args
    return data


@app.route('/', methods=["GET", "POST"])  # GET 和 POST 都可以
def get_data():
    data = request_parse(request)
    # 假设有如下 URL
    # http://10.8.54.48:5000/index?name=john&age=20
    name = data.get("name")
    age = data.get("age")
    print(name, age)


@app.route("/index")
def hello():
    app.logger.info("A user visited the home page >>> %s", session["ctx"])
    app.logger.debug("A debug message")
    return "Hello, World!"


@app.route("/info")
def info():
    app.logger.info("Hello, World!")
    root.debug("A debug message for root")

    extra.debug("A debug message for extra")
    extra.critical("A critical message")

    extra_with_extra.info(
        "A user has visited the home page", extra={"user": "Jack"})

    return "Hello, World! (info)"


@app.route("/warning")
def warning():
    app.logger.warning("A warning message.")
    return "A warning message. (warning)"


@app.before_request
def logBeforeRequest():
    session["ctx"] = {"request_id": str(uuid.uuid4())}
    app.logger.info(
        "path: %s | method: %s >>> %s",
        request.path,
        request.method,
        session["ctx"],
    )


@app.after_request
def logAfterRequest(response):

    app.logger.info(
        "path: %s | method: %s | status: %s | size: %s >>> %s",
        request.path,
        request.method,
        response.status,
        response.content_length,
        session["ctx"],
    )

    return response
