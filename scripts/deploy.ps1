<#
.SYNOPSIS
哇学社自动化部署脚本 (Windows PowerShell)
.DESCRIPTION
启动Docker容器、导入SQL、启动FastAPI服务
#>

$ErrorActionPreference = "Stop"
$ROOT = Split-Path -Parent $PSScriptRoot
$BACKEND = Join-Path $ROOT "backend"
$DATABASE = Join-Path $ROOT "database"

Write-Host "===== 哇学社部署脚本 =====" -ForegroundColor Cyan

# 1. 检查 Docker
Write-Host "[1/5] 检查 Docker..." -ForegroundColor Yellow
try {
    $dockerVersion = docker --version
    Write-Host "  OK: $dockerVersion"
} catch {
    Write-Host "  ERROR: Docker 未安装或不在 PATH 中" -ForegroundColor Red
    exit 1
}

# 2. 启动 Docker 容器
Write-Host "[2/5] 启动 Docker 容器..." -ForegroundColor Yellow
Push-Location $ROOT
try {
    docker compose down 2>$null
    docker compose up -d
    Write-Host "  容器启动中，等待就绪..."
    Start-Sleep -Seconds 15
} finally {
    Pop-Location
}

# 3. 等待 MySQL 就绪
Write-Host "[3/5] 等待 MySQL 就绪..." -ForegroundColor Yellow
$maxRetries = 30
$retryCount = 0
while ($retryCount -lt $maxRetries) {
    try {
        docker exec woxueshe-mysql-1 mysqladmin ping -h localhost -u root -proot123 --silent 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  MySQL 就绪!"
            break
        }
    } catch {}
    $retryCount++
    Start-Sleep -Seconds 2
}
if ($retryCount -eq $maxRetries) {
    Write-Host "  ERROR: MySQL 启动超时" -ForegroundColor Red
    exit 1
}

# 4. 导入初始化 SQL
Write-Host "[4/5] 导入初始化 SQL..." -ForegroundColor Yellow
$sqlFile = Join-Path $DATABASE "init.sql"
$sqlContent = Get-Content $sqlFile -Raw

# 使用 docker exec 导入 SQL
$sqlContent | docker exec -i woxueshe-mysql-1 mysql -u root -proot123 woxueshe 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  SQL 导入成功!" -ForegroundColor Green
} else {
    Write-Host "  WARNING: SQL 导入可能有误，请检查" -ForegroundColor Yellow
}

# 5. 安装后端依赖并启动
Write-Host "[5/5] 安装依赖并启动 API..." -ForegroundColor Yellow
Push-Location $BACKEND
try {
    python -m pip install -r requirements.txt -q 2>&1
    Write-Host "  依赖安装完成"

    # 启动 FastAPI（后台进程）
    $apiLog = Join-Path $ROOT "api.log"
    $job = Start-Job -ScriptBlock {
        param($backendPath, $logFile)
        Set-Location $backendPath
        python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload 2>&1 | Out-File -FilePath $logFile
    } -ArgumentList $BACKEND, $apiLog

    Start-Sleep -Seconds 5
    Write-Host "  API 服务启动中... (日志: $apiLog)"

    # 测试 API
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
        Write-Host "  API 健康检查: $($response.StatusCode)" -ForegroundColor Green
    } catch {
        Write-Host "  WARNING: 健康检查暂未通过，等待服务启动" -ForegroundColor Yellow
    }
} finally {
    Pop-Location
}

Write-Host ""
Write-Host "===== 部署完成 =====" -ForegroundColor Green
Write-Host "API 文档: http://localhost:8000/docs"
Write-Host "MinIO 控制台: http://localhost:9001"
Write-Host "LibreTranslate: http://localhost:5000"
