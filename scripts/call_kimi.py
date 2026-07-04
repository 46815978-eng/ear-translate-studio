#!/usr/bin/env python3
"""
Call Kimi API to generate complete Woxueshe English Learning App codebase.
Outputs are saved as structured markdown files in the project directory.
"""
import json, os, re, sys, time
from openai import OpenAI

API_KEY = "sk-005hTASb5qHLq9BY6SFJeGS6APLJGX4wMHQNF9RHgn46WylH"
BASE_URL = "https://api.moonshot.cn/v1"

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

SYSTEM_PROMPT = """你是一名全栈移动端架构师 + DevOps工程师 + AI音视频工程师。
请一次性完整生成"哇学社英语学习APP"的全部代码和文档。

## 项目概览
一款面向考研/四六级/托福雅思用户的免费英语学习APP，功能包括：AI配音视频课程、听力磨耳朵、FSRS记忆复习、会员订阅。

## 技术要求
- 所有组件必须可运行、无语法错误
- Docker容器配置兼容Windows Docker Desktop
- 所有依赖使用免费开源资源
- MySQL兼容模式设为 ONLY_FULL_GROUP_BY 关闭
- FastAPI使用 ASGI + Uvicorn 启动
- Flutter使用最新稳定版Dart

## 输出格式要求
每个文件以如下标记开始和结束：
```
===FILE: relative/path/to/file.ext ===
文件内容
===END_FILE===
```
所有文件路径相对于项目根目录 /woxueshe/
输出顺序见下方模块清单。

## 模块清单（必须全部生成）

### 模块1: docker-compose.yml
- 服务: MySQL 8.0 (root/root123, 数据库woxueshe, 端口3307)
- Redis 7 (端口6380)
- LibreTranslate (端口5000, 离线翻译)
- MinIO (端口9000/9001, 存储配音/视频/用户头像)
- volumes命名持久化

### 模块2: database/init.sql
建表包含：
- users: id, username, password_hash, email, avatar_url, created_at, updated_at, is_active, is_vip, vip_expire_at
- courses: id, title, description, cover_url, difficulty(enum:beginner/intermediate/advanced), duration_seconds, category, status, created_at
- course_sections: id, course_id, title, content_english, content_chinese, audio_url, video_url, sort_order, duration_seconds
- membership_plans: id, name, price_cents, duration_days, description, features_json, is_active
- user_memberships: id, user_id, plan_id, start_date, end_date, status, payment_method, transaction_id
- study_records: id, user_id, course_id, section_id, study_date, review_count, ease_factor, interval_days, next_review_at, status
- listening_logs: id, user_id, course_id, duration_listened, comprehension_score, completed_at
- payments: id, user_id, amount_cents, payment_method, transaction_id, status, created_at
插入测试数据：3个测试账号、5门课程(每门5-8个section)、3个会员套餐

### 模块3: backend/config.py
FastAPI配置：数据库连接、Redis、MinIO、JWT密钥、Celery Broker URL、LibreTranslate URL

### 模块4: backend/models.py
SQLAlchemy ORM模型对应所有表

### 模块5: backend/schemas.py
Pydantic schemas for request/response

### 模块6: backend/auth.py
JWT认证中间件，注册/登录/刷新token

### 模块7: backend/main.py
FastAPI主应用入口，注册所有路由，CORS配置，生命周期管理

### 模块8: backend/routers/courses.py
课程API: 列表、详情(含sections)、搜索(按难度/分类)

### 模块9: backend/routers/membership.py
会员API: 套餐列表、购买(沙箱)、查询状态、续费

### 模块10: backend/routers/listening.py
听力API: 磨耳朵模式(随机/顺序)、记录进度、获取SRT字幕

### 模块11: backend/routers/review.py
FSRS复习API: 获取待复习列表、提交复习结果、计算下次复习时间

### 模块12: backend/routers/study.py
学习记录API: 记录学时、统计(日/周/月/总)、学习日历

### 模块13: backend/scheduler.py
Celery Beat定时任务配置：每日重置、会员过期检查

### 模块14: backend/tasks/__init__.py
Celery app初始化

### 模块15: backend/tasks/audio_tasks.py
Edge-TTS配音任务、ASMR混音任务、SRT字幕生成

### 模块16: backend/tasks/review_tasks.py
FSRS复习计划计算任务

### 模块17: backend/requirements.txt
所有Python依赖清单

### 模块18: backend/run.py
启动入口: Uvicorn + Celery worker同步启动

### 模块19: render/ffmpeg_render.py
视频渲染脚本：
- 输入: SRT字幕文件 + 音频文件 + 背景(ASMR)音频
- 输出: 16:9 MP4 (纯黑底/可指定纯色背景)
- 字幕: 逐句显示，白色字体，双语可切换
- ASMR背景音音量10%
- 参数化配置

### 模块20: scripts/deploy.sh (Windows兼容使用 .bat/.ps1)
自动化部署脚本：启动Docker、等待容器就绪、导入SQL、启动FastAPI、编译Flutter

### 模块21: scripts/test_pipeline.ps1
自动化测试Pipeline：生成60秒配音→渲染视频→测试API

### 模块22: docs/commercial_migration.md
商用迁移文档：替换Edge-TTS为商用TTS、替换MinIO为阿里云OSS、数据库优化、CDN部署、域名备案等

### 模块23: frontend/ (Flutter完整项目)
完整的Flutter项目，包含：
- pubspec.yaml (包含所有依赖: http, provider, shared_preferences, flutter_secure_storage, audioplayers, video_player, path_provider, flutter_local_notifications, cached_network_image, flutter_svg, lottie, fl_chart, flutter_staggered_animations, shimmer, easy_refresh, 等)
- lib/main.dart (MaterialApp, 路由配置, 主题)
- lib/config/api_config.dart (API地址配置)
- lib/config/theme.dart (主题配置, 哇学社品牌色#4A90D9)
- lib/models/ 所有数据模型
- lib/services/api_service.dart (HTTP客户端, JWT自动刷新)
- lib/providers/ 状态管理
- lib/screens/splash_screen.dart
- lib/screens/login_screen.dart
- lib/screens/register_screen.dart
- lib/screens/home_screen.dart (首页: 推荐课程、每日听力、学习统计)
- lib/screens/course_list_screen.dart (课程列表, 难度/分类筛选)
- lib/screens/course_detail_screen.dart (课程详情, 章节列表)
- lib/screens/listening_screen.dart (磨耳朵播放器: 音频+双语字幕同步)
- lib/screens/review_screen.dart (FSRS复习卡片)
- lib/screens/membership_screen.dart (会员商城, 购买)
- lib/screens/payment_screen.dart (微信/支付宝沙箱)
- lib/screens/profile_screen.dart (个人中心)
- lib/screens/study_stats_screen.dart (学习统计图表)
- lib/widgets/ 所有可复用组件
- android/app/build.gradle (配置应用签名, 包名com.woxueshe.app)
- 全中文UI界面
- 暗色模式支持
- Material 3设计

## 重要约束
1. 所有代码必须是完整的、生产级的，不能有占位符或TODO
2. Flutter代码必须能通过flutter analyze无严重错误
3. FastAPI代码必须能在Python3.11正常运行
4. 所有数据库外键约束正确
5. 密码使用bcrypt哈希
6. JWT token有效期24小时
7. 所有API统一返回格式: {"code": 0, "message": "success", "data": {...}}
8. 分页API统一返回: {"code": 0, "data": {"items": [], "total": 0, "page": 1, "page_size": 20}}
9. FSRS参数: 初始间隔4小时, 默认难度0.3, 稳定阈值2.5
10. Edge-TTS语言参数: 英文语音使用 en-US-JennyNeural, 中文使用 zh-CN-XiaoxiaoNeural"""


def call_kimi(prompt, max_tokens=32000):
    """Call Kimi API with the prompt."""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]
    
    print("[Kimi] Sending request...")
    try:
        response = client.chat.completions.create(
            model="moonshot-v1-auto",
            messages=messages,
            max_tokens=max_tokens,
            temperature=0.3,
            stream=False
        )
        content = response.choices[0].message.content
        print(f"[Kimi] Received response: {len(content)} chars")
        return content
    except Exception as e:
        print(f"[Kimi] Error: {e}")
        return None


def parse_files(content):
    """Parse ===FILE: ... === markers from Kimi output and return dict of {path: content}"""
    files = {}
    pattern = r'===FILE:\s*(.+?)===\s*(.*?)===END_FILE==='
    matches = re.findall(pattern, content, re.DOTALL)
    for path, file_content in matches:
        path = path.strip()
        file_content = file_content.strip()
        files[path] = file_content
        print(f"  -> Parsed: {path} ({len(file_content)} chars)")
    return files


def save_files(files, base_dir):
    """Save parsed files to disk."""
    saved = []
    for path, content in files.items():
        full_path = os.path.join(base_dir, path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content)
        saved.append(path)
    return saved


def main():
    prompt = """请生成"哇学社英语学习APP"所有22个模块的完整代码。
    
请严格按照===FILE: relative/path=== / ===END_FILE=== 格式输出每个文件。

特别注意：
1. Flutter项目需要完整的android/和ios/配置
2. API密钥使用环境变量
3. 所有密码示例使用test123456
4. 测试账号: teacher1/pass, student1/pass, student2/pass
"""

    print("=" * 60)
    print("Kimi Code Generator - Woxueshe English Learning App")
    print("=" * 60)
    
    # Round 1: docker-compose, SQL, backend, render, scripts, docs
    print("\n>>> ROUND 1: Infrastructure + Backend")
    content1 = call_kimi(prompt + "\n\n请先输出模块1-22的全部内容。如果内容较长，可以分批输出。\n本次请输出: 模块1(docker-compose), 模块2(SQL), 模块3-18(全部后端), 模块19(ffmpeg_render), 模块20-22(scripts+docs)")
    
    if not content1:
        print("[ERROR] Round 1 failed")
        sys.exit(1)
    
    files1 = parse_files(content1)
    saved1 = save_files(files1, OUTPUT_DIR)
    print(f"\n[Round 1] Saved {len(saved1)} files")
    
    # Check if Flutter frontend is missing
    has_flutter = any('frontend' in f for f in saved1)
    
    if not has_flutter:
        print("\n>>> ROUND 2: Flutter Frontend")
        content2 = call_kimi("""
请输出"哇学社英语学习APP"的完整Flutter前端代码，必须包含如下文件：

1. pubspec.yaml
2. lib/main.dart (MaterialApp, 路由, 主题, 全局provider)
3. lib/config/api_config.dart
4. lib/config/theme.dart (哇学社品牌色 #4A90D9, Material 3, 暗色模式)
5. lib/models/user_model.dart
6. lib/models/course_model.dart
7. lib/models/membership_model.dart
8. lib/models/study_record_model.dart
9. lib/services/api_service.dart (JWT自动刷新, HTTP封装)
10. lib/providers/auth_provider.dart
11. lib/providers/course_provider.dart
12. lib/providers/study_provider.dart
13. lib/providers/membership_provider.dart
14. lib/screens/splash_screen.dart
15. lib/screens/login_screen.dart
16. lib/screens/register_screen.dart
17. lib/screens/home_screen.dart (首页)
18. lib/screens/course_list_screen.dart
19. lib/screens/course_detail_screen.dart
20. lib/screens/listening_screen.dart (磨耳朵播放器, 双语字幕同步)
21. lib/screens/review_screen.dart (FSRS复习卡片)
22. lib/screens/membership_screen.dart
23. lib/screens/payment_screen.dart
24. lib/screens/profile_screen.dart
25. lib/screens/study_stats_screen.dart
26. lib/widgets/common_widgets.dart
27. android/app/build.gradle (包名com.woxueshe.app)
28. android/settings.gradle
29. android/build.gradle
30. android/gradle.properties

全中文UI界面, Material 3设计, 暗色模式支持。
          
请严格按照===FILE: frontend/path/to/file=== 格式输出。
        """)
        
        if content2:
            files2 = parse_files(content2)
            saved2 = save_files(files2, OUTPUT_DIR)
            print(f"\n[Round 2] Saved {len(saved2)} Flutter files")
        else:
            print("[ERROR] Round 2 failed")
    
    # Summary
    print("\n" + "=" * 60)
    print("GENERATION SUMMARY")
    print("=" * 60)
    
    # List all saved files
    all_files = []
    for root, dirs, files in os.walk(OUTPUT_DIR):
        for f in files:
            rel = os.path.relpath(os.path.join(root, f), OUTPUT_DIR)
            if rel.startswith('scripts' + os.sep + 'call_kimi'):
                continue
            all_files.append(rel)
    
    # Group by module
    modules = {
        'docker': [f for f in all_files if 'docker' in f.lower()],
        'database': [f for f in all_files if f.startswith('database')],
        'backend': [f for f in all_files if f.startswith('backend')],
        'frontend': [f for f in all_files if f.startswith('frontend')],
        'render': [f for f in all_files if f.startswith('render')],
        'scripts': [f for f in all_files if f.startswith('scripts') and 'call_kimi' not in f],
        'docs': [f for f in all_files if f.startswith('docs')],
    }
    
    for mod, files in modules.items():
        if files:
            print(f"  [{mod.upper()}] {len(files)} files:")
            for f in files:
                size = os.path.getsize(os.path.join(OUTPUT_DIR, f))
                print(f"    {f} ({size} bytes)")
        else:
            print(f"  [{mod.upper()}] MISSING!")
    
    # Save generation report
    report_path = os.path.join(OUTPUT_DIR, 'docs', 'generation_report.json')
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            'total_files': len(all_files),
            'modules': {mod: files for mod, files in modules.items()},
            'generation_time': time.strftime('%Y-%m-%d %H:%M:%S'),
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\nReport saved: {report_path}")
    print("Generation complete!")


if __name__ == '__main__':
    main()
