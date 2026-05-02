Write-Host "🔍 Starting Analysis System..." -ForegroundColor Green
Set-Location $PSScriptRoot
..\venv\Scripts\python.exe run_analysis.py
Read-Host "Press Enter to exit"
