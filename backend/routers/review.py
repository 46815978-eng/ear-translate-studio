"""FSRS 复习API路由"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from backend.config import get_db
from backend import models, schemas
from backend.auth import get_current_active_user

router = APIRouter()

# FSRS 默认参数
FSRS_DEFAULT_EASE = 2.5
FSRS_INITIAL_INTERVAL_HOURS = 4
FSRS_STABILITY_THRESHOLD = 2.5


@router.get("/due")
def get_due_reviews(
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """获取待复习列表（FSRS算法）"""
    now = datetime.utcnow()
    records = db.query(models.StudyRecord).filter(
        models.StudyRecord.user_id == current_user.id,
        models.StudyRecord.status == 'active',
        models.StudyRecord.next_review_at <= now,
    ).order_by(models.StudyRecord.next_review_at.asc()).all()
    return {"code": 0, "message": "success", "data": records}


@router.post("/submit")
def submit_review(
    record_id: int,
    quality: int = Query(..., ge=0, le=5, description="复习质量评分 0-5"),
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """
    提交复习结果 (FSRS)
    quality: 0=完全忘记, 1=勉强, 2=困难, 3=良好, 4=熟练, 5=精通
    """
    record = db.query(models.StudyRecord).filter(
        models.StudyRecord.id == record_id,
        models.StudyRecord.user_id == current_user.id,
    ).first()
    if not record:
        raise HTTPException(status_code=404, detail="复习记录不存在")

    # FSRS 核心算法
    record.review_count += 1

    if quality <= 1:
        # 忘记：重置间隔
        new_interval = timedelta(hours=FSRS_INITIAL_INTERVAL_HOURS)
        record.ease_factor = max(1.3, record.ease_factor - 0.2)
    elif quality == 2:
        # 困难：间隔减半
        new_interval = timedelta(days=max(1, record.interval_days // 2))
        record.ease_factor = max(1.3, record.ease_factor - 0.15)
    elif quality == 3:
        # 良好：标准间隔
        new_interval = timedelta(days=max(1, record.interval_days))
        record.ease_factor = max(1.3, record.ease_factor - 0.1)
    elif quality >= 4:
        # 熟练/精通：延长间隔
        if record.review_count == 1:
            interval_hours = max(FSRS_INITIAL_INTERVAL_HOURS, 1)
            new_interval = timedelta(hours=interval_hours)
        else:
            new_interval = timedelta(days=max(1, int(record.interval_days * record.ease_factor)))
        record.ease_factor = min(5.0, record.ease_factor + 0.2 + (quality - 4) * 0.1)

    record.interval_days = new_interval.days if new_interval.days > 0 else 0
    record.next_review_at = datetime.utcnow() + new_interval
    record.study_date = datetime.utcnow()

    db.commit()
    db.refresh(record)
    return {"code": 0, "message": "success", "data": record}


@router.get("/stats")
def get_review_stats(
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """获取复习统计"""
    total = db.query(models.StudyRecord).filter(
        models.StudyRecord.user_id == current_user.id
    ).count()

    due = db.query(models.StudyRecord).filter(
        models.StudyRecord.user_id == current_user.id,
        models.StudyRecord.status == 'active',
        models.StudyRecord.next_review_at <= datetime.utcnow(),
    ).count()

    mastered = db.query(models.StudyRecord).filter(
        models.StudyRecord.user_id == current_user.id,
        models.StudyRecord.status == 'active',
        models.StudyRecord.interval_days >= 21,
    ).count()

    return {"code": 0, "message": "success", "data": {
        "total_records": total,
        "due_reviews": due,
        "mastered": mastered,
        "retention_rate": round(mastered / max(total, 1) * 100, 1),
    }}
