@echo off
echo 📊 GEMS SYSTEM - VISUALIZADOR INTERATIVO
echo ========================================
cd /d "%~dp0"
echo 📂 Diretório: %CD%
echo.
echo 🚀 Executando visualizer...
c:\market_montrezor_system\.venv\Scripts\python.exe visualizer.py
pause
