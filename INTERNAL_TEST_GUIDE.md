# 磨耳AI课堂 - 内测启动指南

## 快速启动（3 步）

### 1. 启动后端（FastAPI）
```bash
cd woxueshe\backend
python -m uvicorn main:app --host 0.0.0.0 --port 8002
```
或双击 `backend\start_server.bat`（如已创建）

后端运行在: http://localhost:8002
API 文档: http://localhost:8002/docs

### 2. 启动前端（Web 版）
双击 `frontend\run_inner_test.bat`
或手动：
```bash
cd woxueshe\frontend\build\web
python -m http.server 8080
```
浏览器访问: http://localhost:8080

### 3. 登录
- 用户名: `student1` / 密码: `test123456`
- 或注册新用户

---

## 功能状态

| 功能 | 状态 | 说明 |
|------|------|------|
| 登录/注册 | ✅ 完成 | 连接真实 API |
| 课程列表 | ✅ 完成 | 连接真实 API |
| 会员中心 | ✅ 完成 | 连接真实 API |
| 首页 | ✅ 完成 | 显示课程 + 功能入口 |
| 磨耳朵 | ✅ 完成 | 连接 `/listening/courses` API |
| 复习 | ✅ 完成 | 连接 `/review/due` API，可提交复习结果 |
| 学习统计 | ✅ 完成 | fl_chart 图表展示 |
| 课程详情 | 🔧 框架完成 | 待完善章节列表 |

---

## APK 构建（内测分发）

### 方式一：安装 Android Studio（推荐）
1. 下载: https://developer.android.com/studio
2. 打开 `woxueshe/frontend` 目录
3. 终端运行: `flutter build apk --release`
4. APK 输出: `frontend/build/app/outputs/flutter-apk/app-release.apk`

### 方式二：命令行（需 Android SDK）
```bash
# 设置环境变量
set ANDROID_HOME=C:\Android\Sdk
set PATH=%PATH%;%ANDROID_HOME%\cmdline-tools\latest\bin

# 安装构建工具
sdkmanager "build-tools;34.0.0" "platform-tools" "platforms;android-33"

# 构建
flutter build apk --release
```

---

## 测试账号

| 用户名 | 密码 | 角色 |
|--------|------|------|
| teacher1 | test123456 | 教师 |
| student1 | test123456 | 学生（有会员记录） |
| student2 | test123456 | 学生 |

---

## 项目结构

```
woxueshe/
├── backend/              # FastAPI 后端（Python）
│   ├── main.py           # 入口
│   ├── routers/          # API 路由
│   ├── models.py         # 数据库模型
│   └── requirements.txt  # Python 依赖
├── frontend/             # Flutter 前端（Dart）
│   ├── lib/              # 源码
│   ├── build/web/        # Web 构建产物（已编译）
│   └── run_inner_test.bat  # 内测启动脚本
├── INTERNAL_TEST_GUIDE.md   # 本文档
└── kimi_flutter_fix.txt     # Kimi 优化建议（如有）
```

---

## 常见问题

**Q: 前端连不上后端？**
A: 确认后端运行在 `localhost:8002`，且 `api_config.dart` 中的 `baseUrl` 正确

**Q: Web 版能改端口吗？**
A: 修改 `run_inner_test.bat` 中的端口号，或运行 `python -m http.server <端口>`

**Q: 如何部署到服务器？**
A: 将 `frontend/build/web/` 所有文件上传到任意 Web 服务器（Nginx/Apache/COS等）
   同时修改 `api_config.dart` 中的 `baseUrl` 为服务器地址，重新构建

---

## 联系方式

内测反馈: （填写你的联系方式）
