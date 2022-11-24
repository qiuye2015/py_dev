import json

from flask import Blueprint, Response
from flask_restful import Api

from apps.todo.views import Todo

todo_bp = Blueprint("todo", __name__, url_prefix='/api/v1')
api = Api(todo_bp)

api.add_resource(Todo, "/todo")


# 由于flask-Restful的返回content-type默认是application/json，
# 所以如果在flask-Restful的视图中想要返回html代码，或者是模板，
# 那么就需要使用api.representation这个装饰器来声明content-type，
# 并且定义一个函数，在这个函数中，应该对html代码进行一个封装，再返回
# [fjp]没有显示调用的地方
# 渲染模版经过修改后，能支持html和json
@api.representation('text/html')
def output_html(data, code, headers):
    if isinstance(data, str):
        # 在representation装饰的函数中，必须返回一个Response对象
        resp = Response(data)
        return resp
    else:
        return Response(json.dumps(data), mimetype='application/json')
