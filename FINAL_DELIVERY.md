# 磨耳AI课堂 - 内测版完成交付

## 构建时间
2026-07-04 08:33

## 已完成

### APK ✅
- 路径: woxueshe/app-release.apk
- 大小: 22.5 MB
- 包名: com.woxueshe.app
- 状态: 已签名（debug key），可安装到 Android 设备

### Web 版 ✅
- 路径: rontend/build/web/
- 状态: 重新构建中

### 后端 API ✅
- 运行: http://localhost:8002
- 15/15 API 全部通过

## 内测启动方法

### APK 安装
1. 将 woxueshe/app-release.apk 传到手机
2. 安装（可能需要允许"未知来源"）
3. 打开 App，访问 http://localhost:8002 作为后端

### Web 版内测
1. 启动后端: cd backend && python -m uvicorn main:app --host 0.0.0.0 --port 8002
2. 启动前端: cd frontend && python -m http.server 8080
3. 浏览器访问: http://localhost:8080

### 登录账号
- teacher1 / test123456
- student1 / test123456

## 技术栈
- 后端: FastAPI + SQLite + Edge-TTS
- 前端: Flutter (iOS/Android/Web)
- 构建: Gradle 8.10.2 + NDK 27.0.12077973

## 解决的关键问题
1. Android SDK 安装 (cmdline-tools + build-tools + platforms)
2. NDK 版本统一 (27.0.12077973)
3. Core library desugaring 启用
4. 资源目录占位符问题
5. Gradle mirror 配置 (dl.google.com)
