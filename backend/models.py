"""SQLAlchemy ORM 模型"""
from sqlalchemy import (
    Column, Integer, String, Text, Enum, DateTime, Float, ForeignKey, JSON, Boolean
)
from sqlalchemy.orm import relationship
from datetime import datetime

from backend.config import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    avatar_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_vip = Column(Boolean, default=False, nullable=False)
    vip_expire_at = Column(DateTime, nullable=True)

    study_records = relationship('StudyRecord', back_populates='user')
    listening_logs = relationship('ListeningLog', back_populates='user')
    user_memberships = relationship('UserMembership', back_populates='user')
    payments = relationship('Payment', back_populates='user')


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    cover_url = Column(String(255), nullable=True)
    difficulty = Column(Enum('beginner', 'intermediate', 'advanced'), nullable=False)
    duration_seconds = Column(Integer, nullable=False, default=0)
    category = Column(String(50), nullable=False)
    status = Column(String(50), nullable=False, default='active')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    course_sections = relationship('CourseSection', back_populates='course', order_by='CourseSection.sort_order')


class CourseSection(Base):
    __tablename__ = 'course_sections'

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    title = Column(String(100), nullable=False)
    content_english = Column(Text, nullable=True)
    content_chinese = Column(Text, nullable=True)
    audio_url = Column(String(255), nullable=True)
    video_url = Column(String(255), nullable=True)
    sort_order = Column(Integer, nullable=False, default=0)
    duration_seconds = Column(Integer, nullable=False, default=0)

    course = relationship('Course', back_populates='course_sections')


class MembershipPlan(Base):
    __tablename__ = 'membership_plans'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price_cents = Column(Integer, nullable=False)
    duration_days = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    features_json = Column(JSON, nullable=False, default=dict)
    is_active = Column(Boolean, default=True, nullable=False)

    user_memberships = relationship('UserMembership', back_populates='plan')


class UserMembership(Base):
    __tablename__ = 'user_memberships'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    plan_id = Column(Integer, ForeignKey('membership_plans.id'), nullable=False)
    start_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_date = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False, default='active')
    payment_method = Column(String(50), nullable=True)
    transaction_id = Column(String(100), nullable=True)

    user = relationship('User', back_populates='user_memberships')
    plan = relationship('MembershipPlan', back_populates='user_memberships')


class StudyRecord(Base):
    __tablename__ = 'study_records'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    section_id = Column(Integer, ForeignKey('course_sections.id'), nullable=True)
    study_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    review_count = Column(Integer, default=0, nullable=False)
    ease_factor = Column(Float, default=2.5, nullable=False)
    interval_days = Column(Integer, default=4, nullable=False)
    next_review_at = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=False, default='active')

    user = relationship('User', back_populates='study_records')
    course = relationship('Course')


class ListeningLog(Base):
    __tablename__ = 'listening_logs'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    duration_listened = Column(Integer, nullable=False, default=0)
    comprehension_score = Column(Float, nullable=False, default=0.0)
    completed_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship('User', back_populates='listening_logs')
    course = relationship('Course')


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount_cents = Column(Integer, nullable=False)
    payment_method = Column(String(50), nullable=False)
    transaction_id = Column(String(100), nullable=False)
    status = Column(String(50), nullable=False, default='pending')
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship('User', back_populates='payments')
