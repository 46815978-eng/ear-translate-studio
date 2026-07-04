"""Celery 任务模块"""
from celery import Celery
from ..config import CELERY_BROKER_URL, CELERY_RESULT_BACKEND

celery_app = Celery(
    'woxueshe',
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=['backend.tasks.audio_tasks', 'backend.tasks.review_tasks'],
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Asia/Shanghai',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit=25 * 60,
)
