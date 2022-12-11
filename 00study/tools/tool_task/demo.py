import time

from pytz import utc
from apscheduler.schedulers.background import BackgroundScheduler
# from apscheduler.jobstores.mongodb import MongoDBJobStore
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
# import logging
#
# logging.basicConfig()
# logging.getLogger('apscheduler').setLevel(logging.DEBUG)

# 一个名为 mongo 的 job 存储，后端使用 MongoDB
# 一个名为 default 的 job 存储，后端使用数据库（使用 Sqlite）
# 一个名为 default 的线程池执行器，最大线程数 20 个
# 一个名为 processpool 的进程池执行器，最大进程数 5 个
# 调度器使用 UTC 时区
# 开启 job 合并
# job 最大实例限制为 3 个一个名为 mongo 的 job 存储，后端使用 MongoDB
# 一个名为 default 的 job 存储，后端使用数据库（使用 Sqlite）
# 一个名为 default 的线程池执行器，最大线程数 20 个
# 一个名为 processpool 的进程池执行器，最大进程数 5 个
# 调度器使用 UTC 时区
# 开启 job 合并
# job 最大实例限制为 3 个
jobstores = {
    # 'mongo': MongoDBJobStore(),
    # 'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}

executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce': False,
    # 当由于某种原因导致某个 job 积攒了好几次没有实际运行.如果 coalesce 为 True，下次这个 job 被 submit 给 executor 时，只会执行 1 次，也就是最后这次
    'max_instances': 3  # 默认情况下，每个 job 仅允许 1 个实例同时运行。这意味着，如果该 job 将要运行，但是前一个实例尚未完成，则最新的 job 不会调度
}

scheduler = BackgroundScheduler(jobstores=jobstores,
                                executors=executors,
                                job_defaults=job_defaults,
                                timezone=utc)
scheduler.start()


def job1():
    print('job1')


def job2():
    print('job2')


# 添加 job
# 1.使用方法 add_job()
# 2.使用装饰器 scheduled_job()
# 第一种是最常用方法，第二种方法适合程序运行后不需要更改的作业。


# 每 10 秒运行一次
scheduler.add_job(
    job1,
    trigger='cron',
    second='*/10'
)

# 每 2 小时运行一次
scheduler.add_job(
    job2,
    trigger='interval',
    seconds=2
)

# scheduler.add_job(myfunc, 'interval', minutes=2, id='my_job_id')
# scheduler.remove_job('my_job_id')

# scheduler.shutdown()

time.sleep(100)
