"""FSRS 复习计划计算任务"""
from celery import shared_task
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from ..config import SessionLocal
from .. import models


@shared_task
def schedule_fsrs_reviews():
    """为每个用户预计算下批复习计划"""
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        # 查找需要安排复习的用户
        users = db.query(models.User).filter(models.User.is_active == True).all()
        scheduled = 0
        for user in users:
            due_records = db.query(models.StudyRecord).filter(
                models.StudyRecord.user_id == user.id,
                models.StudyRecord.status == 'active',
                models.StudyRecord.next_review_at <= now,
            ).count()
            if due_records > 0:
                scheduled += due_records
        return f"Scheduled {scheduled} reviews for {len(users)} users"
    finally:
        db.close()
