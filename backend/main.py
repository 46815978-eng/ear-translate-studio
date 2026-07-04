"""哇学社英语学习APP - FastAPI 主入口"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from backend.config import get_db
from backend.auth import (
    create_access_token, authenticate_user,
    get_current_active_user
)
from backend.routers import courses, membership, listening, review, study, auth_router

app = FastAPI(
    title="哇学社英语学习API",
    description="WoXueShe English Learning App Backend",
    version="1.0.0",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth_router.router, prefix="/auth", tags=["认证"])
app.include_router(courses.router, prefix="/courses", tags=["课程"])
app.include_router(membership.router, prefix="/membership", tags=["会员"])
app.include_router(listening.router, prefix="/listening", tags=["磨耳朵"])
app.include_router(review.router, prefix="/review", tags=["FSRS复习"])
app.include_router(study.router, prefix="/study", tags=["学习记录"])


@app.get("/")
def root():
    return {"message": "哇学社英语学习API", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "ok"}
