#!/bin/bash

# 启动Docker容器
docker-compose up -d

# 等待容器就绪
sleep 10

# 导入SQL
mysql -h localhost -P 3307 -u root -proot123 woxueshe < database/init.sql

# 启动FastAPI
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# 编译Flutter
cd frontend
flutter build apk