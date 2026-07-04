"""FastAPI + SQLAlchemy 配置
支持多模式:
- SQLite: 开发/测试模式，零配置
- MySQL: Docker/本地安装模式
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 数据库模式: sqlite | mysql | auto
DB_MODE = os.getenv('DB_MODE', 'sqlite').lower()

if DB_MODE == 'mysql':
    DATABASE_URL = os.getenv('DATABASE_URL',
        'mysql+pymysql://root:root123@127.0.0.1:3306/woxueshe?charset=utf8mb4')
else:
    # SQLite 模式（默认，无需安装数据库）
    DB_PATH = os.getenv('SQLITE_PATH', os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'data', 'woxueshe.db'
    ))
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    DATABASE_URL = f'sqlite:///{DB_PATH}'

engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    connect_args={'check_same_thread': False} if DB_MODE != 'mysql' else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# JWT 配置
SECRET_KEY = os.getenv('SECRET_KEY', 'woxueshe-jwt-secret-key-2026-v1!!')
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'woxueshe-jwt-secret-key-2026-v1!!')
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24小时
JWT_ALGORITHM = 'HS256'

# Redis
REDIS_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6380/0')

# MinIO (或本地文件存储)
MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', '127.0.0.1:9000')
MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin')
MINIO_BUCKET_NAME = os.getenv('MINIO_BUCKET_NAME', 'woxueshe')
MINIO_SECURE = os.getenv('MINIO_SECURE', 'false').lower() == 'true'

# Celery
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6380/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://127.0.0.1:6380/0')

# LibreTranslate
LIBRETRANSLATE_URL = os.getenv('LIBRETRANSLATE_URL', 'http://127.0.0.1:5000')


def get_db():
    """FastAPI dependency: 获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """初始化数据库：创建所有表和测试数据"""
    from . import models
    Base.metadata.create_all(bind=engine)
    return engine
