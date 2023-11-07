# from apscheduler.schedulers.background import BackgroundScheduler
#
#
# def job():
#     print("Running job...")
#
#
# scheduler = BackgroundScheduler(max_instances=2)
# scheduler.add_job(job, 'interval', seconds=5)
# scheduler.add_job(job, 'interval', seconds=5)
# scheduler.add_job(job, 'interval', seconds=5)
# scheduler.start()
#
# while True:
#     pass


from apscheduler.schedulers.background import BackgroundScheduler


def job():
    print('Job start')
    import time

    time.sleep(10)
    print('Job end')


scheduler = BackgroundScheduler()
scheduler.add_job(job, 'interval', seconds=2, max_instances=2)
scheduler.start()

while True:
    pass
# Execution of job "job (trigger: interval[0:00:02], next run at: 2023-06-06 23:09:44 CST)"
# skipped: maximum number of running instances reached (2)
