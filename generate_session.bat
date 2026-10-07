@echo off
title Telegram String Session Generator - Forwarding Bot
cd /d "%~dp0"
echo ==========================================================
echo Starting Telegram String Session Generator...
echo ==========================================================
python generate_session_string.py
pause
