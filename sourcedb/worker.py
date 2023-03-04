import os
import time

from celery import Celery
from celery.exceptions import SoftTimeLimitExceeded
import celeryconfig

celery = Celery(__name__)
celery.config_from_object(celeryconfig)

@celery.task(name="create_task",time_limit=25)
def create_task(task_type):
    try:
        time.sleep(int(task_type) * 10)
        return True
    except SoftTimeLimitExceeded:
        pass
