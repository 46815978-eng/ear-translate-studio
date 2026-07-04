"""学习记录API路由"""
from fastapi import APIRouter, Depends, HTTPException, Query, Form
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from datetime import datetime, timedelta, date

from backend.config import get_db
from backend import models, schemas
from backend.auth import get_current_active_user

router = APIRouter()


@router.post("/record")
def record_study(
    course_id: int = Form(...),
    section_id: Optional[int] = Form(None),
    duration_seconds: int = Form(0),
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """记录学习时间"""
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")

    now = datetime.utcnow()
    record = models.StudyRecord(
        user_id=current_user.id,
        course_id=course_id,
        section_id=section_id,
        study_date=now,
        review_count=0,
        ease_factor=2.5,
        interval_days=0,
        next_review_at=now + timedelta(hours=4),  # FSRS初始间隔
        status="active",
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return {"code": 0, "message": "success", "data": record}


@router.get("/daily", response_model=dict)
def get_daily_stats(
    date_str: Optional[str] = Query(None, description="日期 YYYY-MM-DD"),
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """获取日学习统计"""
    target_date = datetime.strptime(date_str, "%Y-%m-%d") if date_str else datetime.utcnow()
    next_date = target_date + timedelta(days=1)

    records = db.query(models.StudyRecord).filter(
        models.StudyRecord.user_id == current_user.id,
        models.StudyRecord.study_date >= target_date,
        models.StudyRecord.study_date < next_date,
    ).all()

    total_seconds = sum(
        db.query(models.CourseSection.duration_seconds)
        .filter(models.CourseSection.id == r.section_id)
        .scalar() or 0 for r in records if r.section_id
    )

    return {"code": 0, "message": "success", "data": {
        "date": target_date.strftime("%Y-%m-%d"),
        "records_count": len(records),
        "study_seconds": total_seconds,
        "study_minutes": round(total_seconds / 60, 1),
    }}


@router.get("/weekly", response_model=List[dict])
def get_weekly_stats(
    year: int = Query(datetime.utcnow().year),
    month: int = Query(datetime.utcnow().month),
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """获取周/月学习统计"""
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    results = (
        db.query(
            func.date(models.StudyRecord.study_date).label("study_day"),
            func.count(models.StudyRecord.id).label("count"),
        )
        .filter(
            models.StudyRecord.user_id == current_user.id,
            models.StudyRecord.study_date >= start_date,
            models.StudyRecord.study_date < end_date,
        )
        .group_by(func.date(models.StudyRecord.study_date))
        .all()
    )

    return {"code": 0, "message": "success", "data": [
        {"day": str(r.study_day), "count": r.count}
        for r in results
    ]}


@router.get("/total", response_model=dict)
def get_total_stats(
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """获取总学习统计"""
    total_records = db.query(models.StudyRecord).filter(
        models.StudyRecord.user_id == current_user.id
    ).count()
    total_courses = db.query(models.StudyRecord.course_id).filter(
        models.StudyRecord.user_id == current_user.id
    ).distinct().count()
    total_due = db.query(models.StudyRecord).filter(
        models.StudyRecord.user_id == current_user.id,
        models.StudyRecord.status == 'active',
        models.StudyRecord.next_review_at <= datetime.utcnow(),
    ).count()

    return {"code": 0, "message": "success", "data": {
        "total_records": total_records,
        "total_courses": total_courses,
        "due_reviews": total_due,
    }}


@router.get("/calendar", response_model=List[dict])
def get_study_calendar(
    year: int = Query(datetime.utcnow().year),
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """获取学习日历（全年打卡数据）"""
    start_date = datetime(year, 1, 1)
    end_date = datetime(year + 1, 1, 1)

    results = (
        db.query(
            func.date(models.StudyRecord.study_date).label("study_day"),
            func.count(models.StudyRecord.id).label("count"),
        )
        .filter(
            models.StudyRecord.user_id == current_user.id,
            models.StudyRecord.study_date >= start_date,
            models.StudyRecord.study_date < end_date,
        )
        .group_by(func.date(models.StudyRecord.study_date))
        .all()
    )

    return {"code": 0, "message": "success", "data": [
        {"date": str(r.study_day), "count": r.count}
        for r in results
    ]}
