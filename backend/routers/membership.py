"""会员API路由"""
from fastapi import APIRouter, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
import uuid

from backend.config import get_db
from backend import models, schemas
from backend.auth import get_current_active_user

router = APIRouter()


@router.get("/plans")
def list_plans(db: Session = Depends(get_db)):
    """获取会员套餐列表"""
    plans = db.query(models.MembershipPlan).filter(models.MembershipPlan.is_active == True).all()
    return {"code": 0, "message": "success", "data": plans}


@router.get("/my")
def my_memberships(
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """获取当前用户会员信息"""
    memberships = db.query(models.UserMembership).filter(
        models.UserMembership.user_id == current_user.id
    ).order_by(models.UserMembership.end_date.desc()).all()
    return {"code": 0, "message": "success", "data": memberships}


@router.post("/purchase")
def purchase_membership(
    plan_id: int = Form(...),
    payment_method: str = Form("sandbox"),
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """购买会员 (沙箱模式)"""
    plan = db.query(models.MembershipPlan).filter(models.MembershipPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="套餐不存在")

    # 沙箱支付 - 生成虚拟交易ID
    transaction_id = f"sandbox_{uuid.uuid4().hex[:16]}"

    # 创建支付记录
    payment = models.Payment(
        user_id=current_user.id,
        amount_cents=plan.price_cents,
        payment_method=payment_method,
        transaction_id=transaction_id,
        status="completed",
    )
    db.add(payment)

    # 创建会员记录
    now = datetime.utcnow()
    membership = models.UserMembership(
        user_id=current_user.id,
        plan_id=plan_id,
        start_date=now,
        end_date=now + timedelta(days=plan.duration_days),
        status="active",
        payment_method=payment_method,
        transaction_id=transaction_id,
    )
    db.add(membership)

    # 更新用户VIP状态
    current_user.is_vip = True
    current_user.vip_expire_at = membership.end_date

    db.commit()
    db.refresh(membership)
    return {"code": 0, "message": "success", "data": membership}


@router.post("/sandpay/{plan_id}", response_model=dict)
def sandbox_payment(
    plan_id: int,
    current_user: models.User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    """微信/支付宝沙箱支付接口"""
    plan = db.query(models.MembershipPlan).filter(models.MembershipPlan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="套餐不存在")

    # 模拟沙箱支付页面
    return {
        "code": 0,
        "message": "沙箱订单已创建",
        "data": {
            "order_id": f"ORD{uuid.uuid4().hex[:12].upper()}",
            "plan_name": plan.name,
            "amount_yuan": plan.price_cents / 100,
            "payment_url": f"sandbox://pay?order_id={uuid.uuid4().hex[:16]}",
        }
    }
