"""认证路由: 注册/登录/刷新token"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.config import get_db
from backend import models, schemas
from backend.auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, authenticate_user, decode_access_token
)

router = APIRouter()


@router.post("/register")
def register(user_data: schemas.UserCreate, db: Session = Depends(get_db)):
    """用户注册"""
    existing = db.query(models.User).filter(
        (models.User.username == user_data.username) |
        (models.User.email == user_data.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="用户名或邮箱已存在")

    user = models.User(
        username=user_data.username,
        password_hash=hash_password(user_data.password),
        email=user_data.email,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"code": 0, "message": "success", "data": user}


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """用户登录，返回 JWT token"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.id, "username": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": schemas.User.model_validate(user)
    }


@router.post("/refresh")
def refresh_token(token_data: dict, db: Session = Depends(get_db)):
    """刷新 JWT token"""
    token = token_data.get("token")
    if not token:
        raise HTTPException(status_code=400, detail="缺少token")
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="无效token")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户不存在")
    new_token = create_access_token(data={"sub": user.id, "username": user.username})
    return {"access_token": new_token, "token_type": "bearer"}


@router.get("/me")
def get_me(current_user: models.User = Depends(get_current_user)):
    """获取当前用户信息"""
    return {"code": 0, "message": "success", "data": current_user}
