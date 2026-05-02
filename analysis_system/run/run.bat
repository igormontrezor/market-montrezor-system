@echo off
echo Starting Analysis System...
cd /d "%~dp0"
..\venv\Scripts\python.exe run_analysis.py
pause
