@echo off
cd /d "%~dp0"
echo Starting 磨耳AI课堂 Backend API...
echo.
echo Installing dependencies...
pip install -r requirements.txt -q
echo.
echo Starting FastAPI server on http://localhost:8002
echo API docs: http://localhost:8002/docs
echo.
python -m uvicorn main:app --host 0.0.0.0 --port 8002 --reload
pause
