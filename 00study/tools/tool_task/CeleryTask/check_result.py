from celery.result import AsyncResult
from celery_task_1 import cel

task_id = '59fc45b2-e00b-417f-9ae6-258c96a6013b'
async_result = AsyncResult(id=task_id, app=cel)

if async_result.successful():
    result = async_result.get()
    print('执行成功:', result)
    # result.forget() # 将结果删除
elif async_result.failed():
    print('执行失败')
elif async_result.status == 'PENDING':
    print('任务等待中被执行')
elif async_result.status == 'RETRY':
    print('任务异常后正在重试')
elif async_result.status == 'STARTED':
    print('任务已经开始被执行')

# get celery-task-meta-59fc45b2-e00b-417f-9ae6-258c96a6013b
# {
#     "status": "SUCCESS",
#     "result": "ok",
#     "traceback": null,
#     "children": [],
#     "date_done": "2023-05-19T08:19:16.866296",
#     "task_id": "59fc45b2-e00b-417f-9ae6-258c96a6013b"
# }
