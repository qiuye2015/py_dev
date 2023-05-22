import celery

backend = 'redis://127.0.0.1:6379/1'
broker = 'redis://127.0.0.1:6379/2'

cel = celery.Celery(
    'celery_demo',
    backend=backend,
    broker=broker,
    include=[
        'celery_tasks.task01',
        'celery_tasks.task02',
    ],
)
cel.conf.timezone = 'Asia/Shanghai'
cel.conf.enable_utc = False
