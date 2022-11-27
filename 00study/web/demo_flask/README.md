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

# prepare

```bash
#flask shell
Role.insert_roles()
from apps import fake
fake.users(100)
fake.posts(100)
```

# test

```bash
http --json --auth <email>:<password> GET  http://127.0.0.1:5000/api/v1/posts
```

# QA

1. 收藏夹图标favicon.ico 没有调用