"""数据库初始化 + 测试数据填充"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.config import init_db, SessionLocal, DB_MODE
from backend import models
from backend.auth import hash_password
from datetime import datetime, timedelta


def seed():
    print(f"[Seed] DB mode: {DB_MODE}")
    print("[Seed] Creating tables...")
    init_db()

    db = SessionLocal()
    try:
        # 检查是否已有数据
        existing = db.query(models.User).first()
        if existing:
            print("[Seed] Data already exists, skipping")
            return

        # 创建用户
        pw_hash = hash_password("test123456")
        users = [
            models.User(username="teacher1", password_hash=pw_hash,
                       email="teacher1@woxueshe.com", is_active=True),
            models.User(username="student1", password_hash=pw_hash,
                       email="student1@woxueshe.com", is_active=True),
            models.User(username="student2", password_hash=pw_hash,
                       email="student2@woxueshe.com", is_active=True),
        ]
        db.add_all(users)
        db.flush()

        # 创建课程
        courses = [
            models.Course(title="考研英语核心词汇",
                         description="精选1000个考研英语高频词汇，搭配语境例句",
                         difficulty="advanced", duration_seconds=7200,
                         category="考研英语", status="active"),
            models.Course(title="四六级听力突破",
                         description="听力专项训练，涵盖历年真题对话与讲座",
                         difficulty="intermediate", duration_seconds=5400,
                         category="四六级", status="active"),
            models.Course(title="托福口语入门",
                         description="从基础发音到流利表达，适合托福初学者",
                         difficulty="beginner", duration_seconds=3600,
                         category="托福", status="active"),
            models.Course(title="雅思写作模板",
                         description="大作文小作文模板与高分句式分析",
                         difficulty="intermediate", duration_seconds=9000,
                         category="雅思", status="active"),
            models.Course(title="日常英语会话",
                         description="覆盖点餐、问路、购物等真实场景",
                         difficulty="beginner", duration_seconds=4800,
                         category="日常口语", status="active"),
        ]
        db.add_all(courses)
        db.flush()

        # 创建章节
        sections_data = [
            (1, "词根词缀法", "Understanding root words and affixes is the key to expanding your vocabulary.",
             "理解词根和词缀是扩展词汇量的关键。", 1, 600),
            (1, "同义词辨析", "Synonyms can have subtle differences in meaning and usage.",
             "同义词在含义和用法上可能有细微差别。", 2, 600),
            (1, "真题例句", "The government has implemented new policies to address environmental concerns.",
             "政府已实施新政策以解决环境问题。", 3, 600),
            (2, "短对话训练", "W: Could you tell me where the library is? M: Sure, go straight and turn left.",
             "女：你能告诉我图书馆在哪里吗？男：当然，直走在第二个路口左转。", 1, 600),
            (2, "长对话训练", "Today we will discuss the impact of social media on modern communication.",
             "今天我们将讨论社交媒体对现代交流的影响。", 2, 600),
            (2, "讲座听力", "Good morning everyone. In today lecture, we will explore climate change.",
             "大家早上好。在今天的讲座中，我们将探讨气候变化。", 3, 600),
            (3, "发音基础", "Pronunciation is the foundation of spoken English.",
             "发音是英语口语的基础。", 1, 600),
            (3, "语调训练", "Rising intonation is used for yes-no questions.",
             "升调用于一般疑问句，降调用于特殊疑问句和陈述句。", 2, 600),
            (4, "大作文结构", "A well-structured essay has three parts: introduction, body, and conclusion.",
             "结构良好的文章包括三部分：引言、正文和结论。", 1, 600),
            (4, "高分句式", "Using complex sentence structures can significantly improve your writing score.",
             "使用复杂句式可以显著提高你的写作分数。", 2, 600),
            (5, "点餐场景", "I would like to order a steak medium rare, please.",
             "我想点一份五分熟的牛排。", 1, 600),
            (5, "问路场景", "Excuse me, how do I get to the nearest subway station?",
             "打扰一下，最近的地铁站怎么走？", 2, 600),
        ]
        sections = []
        for cid, title, eng, chi, sort_order, dur in sections_data:
            section = models.CourseSection(
                course_id=courses[cid-1].id,
                title=title, content_english=eng, content_chinese=chi,
                sort_order=sort_order, duration_seconds=dur
            )
            sections.append(section)
        db.add_all(sections)
        db.flush()

        # 创建会员套餐
        plans = [
            models.MembershipPlan(name="月度会员", price_cents=2900, duration_days=30,
                description="基础学习功能，适合短期冲刺",
                features_json={"ai_dubbing": True, "srt_subtitle": True, "fsrs_review": True,
                              "asmr_mix": True, "listening_mode": "basic", "download_limit": 50}),
            models.MembershipPlan(name="季度会员", price_cents=6900, duration_days=90,
                description="推荐选择，性价比最高",
                features_json={"ai_dubbing": True, "srt_subtitle": True, "fsrs_review": True,
                              "asmr_mix": True, "listening_mode": "advanced",
                              "download_limit": 200, "translation": "full"}),
            models.MembershipPlan(name="年度会员", price_cents=19900, duration_days=365,
                description="全年畅学，送专属学习规划",
                features_json={"ai_dubbing": True, "srt_subtitle": True, "fsrs_review": True,
                              "asmr_mix": True, "listening_mode": "premium", "download_limit": -1,
                              "translation": "full", "study_plan": True, "priority_support": True}),
        ]
        db.add_all(plan for plan in plans)
        db.flush()

        # 给 student1 创建已过期会员
        now = datetime.utcnow()
        expired = models.UserMembership(
            user_id=users[1].id, plan_id=plans[0].id,
            start_date=now - timedelta(days=60),
            end_date=now - timedelta(days=30),
            status="expired", payment_method="sandbox"
        )
        db.add(expired)

        payment = models.Payment(
            user_id=users[1].id, amount_cents=2900,
            payment_method="sandbox", transaction_id="sandbox_seed_001",
            status="completed"
        )
        db.add(payment)

        db.commit()
        print(f"[Seed] Success! Created {len(users)} users, {len(courses)} courses, "
              f"{len(sections)} sections, {len(plans)} plans")
    except Exception as e:
        db.rollback()
        print(f"[Seed] Error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
