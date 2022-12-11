from flask import Flask, jsonify, request

app = Flask(__name__)


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
