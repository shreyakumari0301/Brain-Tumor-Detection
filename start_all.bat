@echo off
echo Starting Brain Tumor Detection System...
echo.
echo Starting Backend Server...
start "Backend Server" cmd /k "cd backend && python main.py"
timeout /t 3 /nobreak >nul
echo.
echo Starting Frontend...
start "Frontend" cmd /k "streamlit run frontend/app.py"
echo.
echo Both servers are starting...
echo Backend: http://localhost:8000
echo Frontend: http://localhost:8501
pause

