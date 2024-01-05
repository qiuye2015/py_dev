# export JAVA_HOME=/opt/homebrew/opt/openjdk@11
# local
# cd apache-seatunnel-2.3.3 && sh ./bin/seatunnel.sh -e local --config ../mysql2kafka.config
# cd apache-seatunnel-2.3.3 && sh ./bin/seatunnel.sh -e local --config ../mysql2es.config

######### cluster-mode ##########
# cd apache-seatunnel-2.3.3 && sh ./bin/seatunnel.sh --config ../mysql2es.config
cd apache-seatunnel-2.3.3 && sh ./bin/seatunnel.sh --config ../mysql2kafka.config

######### web ###########
#export ST_WEB_BASEDIR_PATH=~/workspace/github/icoding/py_dev/DTS_CDC/SeaTunnel/apache-seatunnel-web-1.0.0-bin
#export SEATUNNEL_HOME=~/workspace/github/icoding/py_dev/DTS_CDC/SeaTunnel/apache-seatunnel-2.3.3
# 1. 运行seattunnel Zeta Engine Server, port 5801
# cd apache-seatunnel-2.3.3 && sh bin/seatunnel-cluster.sh -d
# 2. 初始化数据库 apache-seatunnel-web-${project.version}/script/seatunnel_server_env.sh
# cd apache-seatunnel-web-1.0.0-bin && bash script/init_sql.sh
# 3. 运行 SeaTunnel Web
# cd apache-seatunnel-web-1.0.0-bin && sh bin/seatunnel-backend-daemon.sh start
# 4. 在浏览器中访问 http://127.0.0.1:8801/ui/ , 默认用户名和密码是 admin/admin.
