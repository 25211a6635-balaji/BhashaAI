@echo off
title BhashaAI - Indian Dialect AI

echo.
echo ==========================================
echo           BHASHAAI STARTING
echo ==========================================
echo.
echo Please wait while the AI models load...
echo.

cd /d C:\Users\balaj\BhashaAI

start "" http://127.0.0.1:8000

python -m uvicorn app:app --host 127.0.0.1 --port 8000

pause