"""课程API路由"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.config import get_db
from backend import models, schemas

router = APIRouter()


@router.get("/")
def list_courses(
    difficulty: Optional[str] = Query(None, pattern="^(beginner|intermediate|advanced)?$"),
    category: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """获取课程列表，支持按难度/分类筛选和分页"""
    q = db.query(models.Course).filter(models.Course.status == 'active')
    if difficulty:
        q = q.filter(models.Course.difficulty == difficulty)
    if category:
        q = q.filter(models.Course.category == category)
    total = q.count()
    items = q.order_by(models.Course.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {
        "code": 0,
        "message": "success",
        "data": {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
        }
    }


@router.get("/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)):
    """获取课程详情"""
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    return {"code": 0, "message": "success", "data": course}


@router.get("/{course_id}/sections")
def get_course_sections(course_id: int, db: Session = Depends(get_db)):
    """获取课程章节列表"""
    course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="课程不存在")
    return {"code": 0, "message": "success", "data": course.course_sections}
