"""Celery Beat 定时任务"""
from celery import shared_task
from datetime import datetime
from sqlalchemy.orm import Session

from backend.config import SessionLocal
from backend import models


@shared_task
def check_expired_memberships():
    """每日检查会员过期"""
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        expired = db.query(models.UserMembership).filter(
            models.UserMembership.status == 'active',
            models.UserMembership.end_date < now,
        ).all()
        for m in expired:
            m.status = 'expired'
            user = db.query(models.User).filter(models.User.id == m.user_id).first()
            if user:
                user.is_vip = False
        db.commit()
        return f"Checked {len(expired)} expired memberships"
    finally:
        db.close()


@shared_task
def daily_reset():
    """每日重置任务"""
    return "Daily reset completed"
