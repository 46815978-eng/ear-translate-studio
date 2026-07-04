"""Pydantic schemas for request/response"""
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from typing import Optional, List


class UserBase(BaseModel):
    username: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    is_active: bool = True
    is_vip: bool = False
    vip_expire_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class CourseSection(BaseModel):
    id: int
    course_id: int
    title: str
    content_english: Optional[str] = None
    content_chinese: Optional[str] = None
    audio_url: Optional[str] = None
    video_url: Optional[str] = None
    sort_order: int = 0
    duration_seconds: int = 0

    model_config = ConfigDict(from_attributes=True)


class Course(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    cover_url: Optional[str] = None
    difficulty: str
    duration_seconds: int = 0
    category: str
    status: str = 'active'
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MembershipPlan(BaseModel):
    id: int
    name: str
    price_cents: int
    duration_days: int
    description: Optional[str] = None
    features_json: dict = {}
    is_active: bool = True

    model_config = ConfigDict(from_attributes=True)


class UserMembership(BaseModel):
    id: int
    user_id: int
    plan_id: int
    start_date: datetime
    end_date: datetime
    status: str = 'active'
    payment_method: Optional[str] = None
    transaction_id: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class StudyRecord(BaseModel):
    id: int
    user_id: int
    course_id: int
    section_id: Optional[int] = None
    study_date: datetime
    review_count: int = 0
    ease_factor: float = 2.5
    interval_days: int = 0
    next_review_at: Optional[datetime] = None
    status: str = 'active'

    model_config = ConfigDict(from_attributes=True)


class ListeningLog(BaseModel):
    id: int
    user_id: int
    course_id: int
    duration_listened: int = 0
    comprehension_score: float = 0.0
    completed_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Payment(BaseModel):
    id: int
    user_id: int
    amount_cents: int
    payment_method: str
    transaction_id: str
    status: str = 'pending'
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: User


class PaginatedResponse(BaseModel):
    items: List
    total: int
    page: int
    page_size: int
