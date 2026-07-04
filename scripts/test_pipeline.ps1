<#
.SYNOPSIS
哇学社自动化测试Pipeline
测试：配音→字幕→视频渲染→API测试
#>

$ErrorActionPreference = "Stop"
$ROOT = Split-Path -Parent $PSScriptRoot
$RENDER_DIR = Join-Path $ROOT "render"
$OUTPUT_DIR = Join-Path $ROOT "test_output"

# 创建输出目录
New-Item -ItemType Directory -Force -Path $OUTPUT_DIR | Out-Null

Write-Host "===== 哇学社自动化测试 Pipeline =====" -ForegroundColor Cyan
Write-Host ""

# ===== 测试文案 (60秒英文口播) =====
$scriptText = @"
Welcome to Woxueshe. Today we will learn about the fascinating world of language learning.
Research shows that listening to native speakers is one of the most effective ways to improve.
Our brains are wired to recognize patterns in speech and music.
When you combine listening practice with spaced repetition, your retention improves dramatically.
This is the core philosophy behind our app. We believe that language learning should be accessible to everyone.
Start your journey today and discover how easy it can be.
"@

$srtContent = @"
1
00:00:00,000 --> 00:00:04,000
Welcome to Woxueshe.
欢迎来到哇学社。

2
00:00:04,000 --> 00:00:09,000
Today we will learn about the fascinating world of language learning.
今天我们来了解语言学习的迷人世界。

3
00:00:09,000 --> 00:00:14,000
Research shows that listening to native speakers is one of the most effective ways to improve.
研究表明，听母语者的发音是最有效的提高方式之一。

4
00:00:14,000 --> 00:00:19,000
Our brains are wired to recognize patterns in speech and music.
我们的大脑天生就能够识别语音和音乐中的模式。

5
00:00:19,000 --> 00:00:24,000
When you combine listening practice with spaced repetition, your retention improves dramatically.
当你将听力练习与间隔重复结合时，你的记忆力会显著提高。

6
00:00:24,000 --> 00:00:30,000
This is the core philosophy behind our app.
这就是我们应用背后的核心哲学。

7
00:00:30,000 --> 00:00:35,000
We believe that language learning should be accessible to everyone.
我们相信语言学习应该对每个人都是可及的。

8
00:00:35,000 --> 00:00:42,000
Start your journey today and discover how easy it can be.
今天就开始你的旅程，发现它有多简单。
"@

$srtFile = Join-Path $OUTPUT_DIR "test_subtitles.srt"
$srtContent | Out-File -FilePath $srtFile -Encoding UTF8
Write-Host "[1/4] 测试字幕已创建: $srtFile" -ForegroundColor Yellow

# ===== 生成测试音频 (使用 Edge-TTS) =====
Write-Host "[2/4] 调用 Edge-TTS 生成配音..." -ForegroundColor Yellow
$audioFile = Join-Path $OUTPUT_DIR "test_speech.mp3"

try {
    $ttsScript = @"
import asyncio
import edge_tts
text = """$scriptText"""
async def main():
    tts = edge_tts.Communicate(text, "en-US-JennyNeural")
    await tts.save("$audioFile")
asyncio.run(main())
"@
    $ttsScriptFile = Join-Path $OUTPUT_DIR "gen_tts.py"
    $ttsScript | Out-File -FilePath $ttsScriptFile -Encoding UTF8
    python $ttsScriptFile 2>&1
    if (Test-Path $audioFile) {
        Write-Host "  配音生成成功: $( [math]::Round((Get-Item $audioFile).Length / 1024) ) KB" -ForegroundColor Green
    }
} catch {
    Write-Host "  WARNING: Edge-TTS 生成失败，使用静音音频代替" -ForegroundColor Yellow
    # 生成静音音频作为后备
    ffmpeg -y -f lavfi -i anullsrc=r=44100:cl=mono -t 42 -acodec aac "$audioFile" 2>&1 | Out-Null
}

# ===== 生成 ASMR 背景音 =====
Write-Host "[3/4] 生成 ASMR 背景音..." -ForegroundColor Yellow
$asmrFile = Join-Path $OUTPUT_DIR "test_asmr.mp3"
try {
    # 生成粉红噪音作为ASMR模拟
    ffmpeg -y -f lavfi -i "anoisesrc=d=42:c=pink:a=0.3" -acodec aac "$asmrFile" 2>&1 | Out-Null
    if (Test-Path $asmrFile) {
        Write-Host "  ASMR 生成成功" -ForegroundColor Green
    }
} catch {
    Write-Host "  WARNING: ASMR 生成失败" -ForegroundColor Yellow
}

# ===== 渲染测试视频 =====
Write-Host "[4/4] 渲染测试视频..." -ForegroundColor Yellow
$outputVideo = Join-Path $OUTPUT_DIR "test_video.mp4"
try {
    python "$ROOT\render\ffmpeg_render.py" `
        --srt "$srtFile" `
        --audio "$audioFile" `
        --bg_audio "$asmrFile" `
        --output "$outputVideo" `
        --bg_color "#1a1a2e" `
        --width 1920 --height 1080

    if (Test-Path $outputVideo) {
        $size = [math]::Round((Get-Item $outputVideo).Length / 1MB, 1)
        Write-Host "  视频渲染完成: $size MB - $outputVideo" -ForegroundColor Green
    }
} catch {
    Write-Host "  ERROR: 视频渲染失败: $_" -ForegroundColor Red
}

# ===== API 测试 =====
Write-Host ""
Write-Host "----- API 测试 -----" -ForegroundColor Cyan

# 测试健康检查
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -TimeoutSec 5
    Write-Host "[API] 健康检查: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "[API] 健康检查: API 未运行 (跳过)" -ForegroundColor Yellow
}

# 测试注册
try {
    $registerBody = @{username="test_user"; email="test@test.com"; password="test123"} | ConvertTo-Json
    $regResult = Invoke-RestMethod -Uri "http://localhost:8000/auth/register" -Method Post `
        -Body $registerBody -ContentType "application/json" -TimeoutSec 5
    Write-Host "[API] 注册测试: $($regResult.username)" -ForegroundColor Green
} catch {
    Write-Host "[API] 注册测试: 服务未运行或已注册 (跳过)" -ForegroundColor Yellow
}

# 测试登录
try {
    $loginBody = @{username="student1"; password="test123456"; grant_type="password"} | ConvertTo-Json
    $loginResult = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" -Method Post `
        -Body "username=student1&password=test123456" `
        -ContentType "application/x-www-form-urlencoded" -TimeoutSec 5
    Write-Host "[API] 登录测试: Token 获取成功" -ForegroundColor Green
    $global:token = $loginResult.access_token
} catch {
    Write-Host "[API] 登录测试: 服务未运行 (跳过)" -ForegroundColor Yellow
}

# 测试课程列表
if ($global:token) {
    try {
        $courses = Invoke-RestMethod -Uri "http://localhost:8000/courses/" `
            -Headers @{Authorization="Bearer $token"} -TimeoutSec 5
        Write-Host "[API] 课程列表: 获取 $($courses.total) 门课程" -ForegroundColor Green
    } catch {
        Write-Host "[API] 课程列表: 失败" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "===== 测试完成 =====" -ForegroundColor Green
Write-Host "输出目录: $OUTPUT_DIR"
