import logging
import time

from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.background import BackgroundScheduler
from flask_apscheduler import APScheduler

from tools.tool_log.Best_Practices.log import get_logger

executors = {'default': ThreadPoolExecutor(1)}
bs = BackgroundScheduler(timezone="Asia/Shanghai")
scheduler = APScheduler(bs)

logger = get_logger()


@scheduler.task("interval", id="cron_job", seconds=10)
def cron_job():
    logger.warning("test start")
    time.sleep(30)
    logger.warning("test end")


# scheduler.init_app(app)
scheduler.start()
time.sleep(60)
