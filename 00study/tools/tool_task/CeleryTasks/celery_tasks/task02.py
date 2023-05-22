import time

from celery_tasks.celery import cel


@cel.task
def send_msg(name):
    print("向%s发送短信..." % name)
    time.sleep(5)
    return "向%s发送短信完成..." % name
