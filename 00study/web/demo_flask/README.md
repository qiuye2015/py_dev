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
flask test --coverage

http --json --auth leo@qq.com:123 GET  http://127.0.0.1:5000/api/v1/posts
http --auth leo@qq.com:123 --json POST http://127.0.0.1:5000/api/v1/posts/ "body=I'm adding a post from the *command line*."
http --auth leo@qq.com:123 --json POST http://127.0.0.1:5000/api/v1/tokens/
```

# 性能分析

```bash
flask profile
```

# deploy

```bash
gunicorn app:app
```

# sql

```bash
docker run --name mysql -d -e MYSQL_RANDOM_ROOT_PASSWORD=yes \ 
-e MYSQL_DATABASE=flasky -e MYSQL_USER=flasky \
-e MYSQL_PASSWORD=<database-password> \
mysql/mysql-server:5.7

docker run -d -p 8000:5000 --link mysql:dbserver \
-e DATABASE_URL=mysql+pymysql://flasky:<database-password>@dbserver/flasky \
-e MAIL_USERNAME=<your-gmail-username> -e MAIL_PASSWORD=<your-gmail-password> \ 
flasky:latest
# --link 选项把这个新容器与一个现有的容器连接起来。
# --link 选项的值是以冒号分隔的两个名称，
# 一个是目标容器的名称或 ID，另一个是在当前容器中访问目标容器所用的别名
```

# .env

```commandline
FLASK_APP=app.py
FLASK_CONFIG=docker
SECRET_KEY=3128b4588e7f4305b5501025c13ceca5
MAIL_USERNAME=<your-gmail-username>
MAIL_PASSWORD=<your-gmail-password>
DATABASE_URL=mysql+pymysql://flasky:<database-password>@dbserver/flasky
```

# .env-mysql

```commandline
MYSQL_RANDOM_ROOT_PASSWORD=yes
MYSQL_DATABASE=flasky
MYSQL_USER=flasky
MYSQL_PASSWORD=<database-password>
```