@echo off
cd /d "%~dp0"
start http://localhost:8080
python run_web_server.py
