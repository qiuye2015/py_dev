# install

```bash
pip install flask-restful

pip freeze >requirements.txt
pip install -r requirements.txt
```

# run

```bash
export FLASK_APP=app.py
export FLASK_DEBUG=1
flask run
# OR
## app.run()
python3 app.py

flask routes
flask test
flask db init
flask db upgrade

```

# QA

1. 收藏夹图标favicon.ico 没有调用