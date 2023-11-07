import logging
from flask import Flask, request

app = Flask(__name__)

# 设置日志级别为 DEBUG
logging.basicConfig(level=logging.DEBUG)


@app.before_request
def before_request():
    """
    以表单形式multipart/form-data、application/x-www-form-urlencoded 提交的数据，form或者files属性有值
    当content-type不是multipart/form-data、application/x-www-form-urlencoded 这两种类型时，data才会有值
    如果是以application/json提交的数据，data、json就有值。而 args 是通过解析url中的查询参数得来的
    """
    app.logger.debug("*" * 60)
    app.logger.debug('Request Method: %s', request.method)
    app.logger.debug('Request URL: %s', request.url)
    app.logger.debug('Request Base_url: %s', request.base_url)
    app.logger.debug('Request Full_path: %s', request.full_path)
    app.logger.debug('Request Path: %s', request.path)
    app.logger.debug('Request Host: %s', request.host)
    app.logger.debug('Request Endpoint: %s', request.endpoint)
    app.logger.debug('Request Args: %s', request.args)
    # app.logger.debug('Request Headers: %s', request.headers)
    print('Request Headers: %s', request.headers)
    content_type = request.content_type or request.headers.get('Content-Type', '')
    app.logger.debug('Request Content-Type: %s', content_type)

    if 'application/x-www-form-urlencoded' in content_type or 'multipart/form-data' in content_type:
        app.logger.debug('Request Form: %s', request.form)
        app.logger.debug('Request Files: %s', request.files)
        # # 遍历表单数据
        # for key, value in request.form.items():
        #     app.logger.debug(f'{key}: {value} ({type(value).__name__})')
    else:
        # content_type == 'text/plain' / application/xml
        app.logger.debug('Request Data.decode: %s', request.data.decode('utf-8'))
        if content_type == 'application/json':
            app.logger.debug('Request Json: %s', request.json)

    app.logger.debug("*" * 60)


# application/x-www-form-urlencoded：
@app.route('/form', methods=['POST'])
def handle_form_data():
    data = request.form
    return str(data)


# multipart/form-data：
@app.route('/upload', methods=['POST'])
def upload_file():
    file_obj = request.files.get('file')  # 获取上传的文件对象
    if file_obj:
        filename = file_obj.filename
        file_obj.save(filename)  # 将文件保存在当前目录下
        return f'File {filename} uploaded successfully.'

    return 'No file_obj uploaded.'


@app.route('/json', methods=['POST'])
def handle_json_data():
    data = request.get_json()
    return str(data)


@app.route('/text', methods=['POST'])
def handle_plain_text():
    data = request.data.decode('utf-8')
    return data


@app.route('/xml', methods=['POST'])
def handle_xml_data():
    data = request.data.decode('utf-8')
    return data


if __name__ == '__main__':
    app.run(debug=True)
