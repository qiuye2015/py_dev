from datetime import datetime, timedelta

from celery_task_1 import send_email

# result = send_email.delay('yuan')
# print(result.id)
# result2 = send_email.delay('alx')
# print(result2.id)

# v1 = datetime(2023, 5, 19, 22, 6, 00)
# print(v1)
# v2 = datetime.utcfromtimestamp(v1.timestamp())
# print(v2)
# result = send_email.apply_async(args=['fjp'], eta=v2)
# print(result.id)

ctime = datetime.now()
utc_time = datetime.utcfromtimestamp(ctime.timestamp())
time_delay = timedelta(seconds=10)
task_time = utc_time + time_delay
result = send_email.apply_async(args=['fjp'], eta=task_time)
print(result.id)
