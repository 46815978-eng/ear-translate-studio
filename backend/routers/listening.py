"""磨耳朵听力API路由"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import random
from datetime import datetime

from backend.config import get_db, MINIO_ENDPOINT, MINIO_BUCKET_NAME
from backend import models, schemas
from backend.auth import get_current_active_user

router = APIRouter()


@router.get("/courses")
def listening_courses(
    mode: str = Query("random"),
    limit: int = Query(10, ge=1, le=50),
    db: Session = Depends(get_db),
):
    """获取磨耳朵课程列表（随机/顺序模式）"""
    q = db.query(models.Course).filter(models.Course.status == 'active').limit(limit)
    courses = q.all()
    if mode == "random":
        random.shuffle(courses)
    return {
        "code": 0,
        "message": "success",
        "data": {
            "mode": mode,
            "count": len(courses),
            "items": courses,
        }
    }


@router.get("/sections/{course_id}")
def get_sections_for_listening(
    course_id: int,
    db: Session = Depends(get_db),
):
    """获取课程章节（用于听力播放）"""
    sections = db.query(models.CourseSection).filter(
        models.CourseSection.course_id == course_id
    ).order_by(models.CourseSection.sort_order).all()
    if not sections:
        raise HTTPException(status_code=404, detail="该课程暂无章节")
    return {"code": 0, "message": "success", "data": sections}


@router.get("/subtitles/{section_id}", response_model=dict)
def get_subtitles(
    section_id: int,
    db: Session = Depends(get_db),
):
    """获取章节双语字幕"""
    section = db.query(models.CourseSection).filter(models.CourseSection.id == section_id).first()
    if not section:
        raise HTTPException(status_code=404, detail="章节不存在")

    # 自动生成SRT格式字幕（从数据库中英文字段组装）
    srt_lines = []
    idx = 1
    # 模拟逐句字幕，实际可在上课前用Edge-TTS生成
    eng_sentences = (section.content_english or "").split(".")
    chi_sentences = (section.content_chinese or "").split("。")
    duration = section.duration_seconds
    per_line = max(duration // max(len(eng_sentences), 1), 3)

    for i, eng in enumerate(eng_sentences):
        if not eng.strip():
            continue
        start = i * per_line
        end = (i + 1) * per_line
        chinese = chi_sentences[i] if i < len(chi_sentences) else ""
        srt_lines.append(f"{idx}")
        srt_lines.append(f"{_format_srt_time(start)},{_format_srt_time(end)}")
        srt_lines.append(f"{eng.strip()}")
        srt_lines.append(f"{chinese.strip()}")
        srt_lines.append("")
        idx += 1

    return {
        "code": 0, "message": "success",
        "data": {
            "srt": "\n".join(srt_lines),
            "audio_url": section.audio_url,
            "video_url": section.video_url,
            "duration_seconds": section.duration_seconds,
        }
    }


@router.post("/progress")
def record_listening_progress(
    course_id: int,
    duration_listened: int,
    comprehension_score: float = 0.0,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """记录听力进度"""
    log = models.ListeningLog(
        user_id=current_user.id,
        course_id=course_id,
        duration_listened=duration_listened,
        comprehension_score=comprehension_score,
        completed_at=datetime.utcnow(),
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return {"code": 0, "message": "success", "data": log}


def _format_srt_time(seconds: int) -> str:
    """将秒数格式化为SRT时间戳"""
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"
