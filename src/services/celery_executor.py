from celery import Celery
import os

celery_app = Celery('tasks', broker=os.getenv('REDIS_BROKER_URL', 'redis://localhost:6379/0'))

class CeleryExecutor:
    def execute(self, func, data):
        tasks = [run_with_retry.delay(func, d) for d in data]
        return [task.get() for task in tasks]

@celery_app.task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 3})
def run_with_retry(self, func, d):
    return func(d)