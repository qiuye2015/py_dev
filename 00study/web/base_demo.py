from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


def long_running_task(req):
    # 这里是你的耗时任务
    import time
    print("start...")
    time.sleep(10)
    print("end...")
    pass


@app.route('/hello', methods=['GET'])
def your_route():
    import threading
    thread = threading.Thread(target=long_running_task, args=(1,))
    thread.start()
    return {"msg": "Task started"}


if __name__ == '__main__':
    app.run()
