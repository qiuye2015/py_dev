from datetime import datetime

from flask import render_template
from flask_restful import Resource, reqparse


class Todo(Resource):
    def get(self):
        print("*" * 30)
        parser = reqparse.RequestParser()
        # bundle_errors 将所有产生的错误都绑定在一起，然后同时一次性返回给客户端
        # app.config['BUNDLE_ERRORS'] = True
        # python3默认类型是str,python2是unicode
        parser.add_argument('name', required=True, action='append', help="Name cannot be blank!", location='args')
        parser.add_argument('rate', type=int, help='Rate cannot be converted', dest='rate_int')
        # parser.add_argument('file', location='files', type=FileStorage)
        parser.add_argument(
            'foo',
            choices=('one', 'two'),
            help='Bad choice: {error_msg}'
        )
        # action='append' 接受多个值
        # dest='rate_int' 起别名
        # location='args' form headers cookies files json

        # args = parser.parse_args()
        # print("get", args)
        # return "get", 200
        return render_template('index_now.html', current_time=datetime.utcnow()), 200
        # return {'message': 'get '}, 200

    def post(self):
        print("post")
        return 'post', 201

    def put(self):
        print("put")
        return "put", 200

    def patch(self):
        print("patch")
        return "patch", 200

    def delete(self):
        return "", 204
