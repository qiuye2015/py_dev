# Project Layout

```
/home/user/Projects/flask-tutorial
├── flaskr/
│   ├── __init__.py
│   ├── db.py
│   ├── schema.sql
│   ├── auth.py
│   ├── blog.py
│   ├── templates/
│   │   ├── base.html            基本布局
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   └── blog/
│   │       ├── create.html
│   │       ├── index.html
│   │       └── update.html
│   └── static/
│       └── style.css
├── tests/
│   ├── conftest.py
│   ├── data.sql
│   ├── test_factory.py
│   ├── test_db.py
│   ├── test_auth.py
│   └── test_blog.py
├── venv/
├── setup.py        描述了您的项目和属于它的文件
└── MANIFEST.in     复制static和templates 目录和schema.sql文件中的所有内容，但要排除所有字节码文件
```

# Install

```bash
# Create a virtualenv and activate it:
python3 -m venv venv
. venv/bin/activate
# Install Flaskr:
pip install -e .
```

# Run

```bash
flask --app flaskr init-db
flask --app flaskr --debug run
```

# Test

```bash
# pip install pytest coverage
pip install '.[test]'
pytest
```

Run with coverage report:

```bash
coverage run -m pytest
coverage report
coverage html  # open htmlcov/index_now.html in a browser
```

# from

[参考](https://github.com/pallets/flask/tree/main/examples/tutorial)