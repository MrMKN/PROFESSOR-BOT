@echo off
title Push Forwarding Bot to GitHub
cd /d "%~dp0"

echo ==========================================================
echo  Pushing Forwarding_bot to GitHub (Heroku Ready)
echo ==========================================================

if not exist .git (
    echo [*] Initializing Git repository...
    git init -b main
)

echo [*] Checking .gitignore status...
git status --ignored

echo.
set /p REPO_URL="Enter your GitHub repository URL (e.g. https://github.com/USERNAME/REPO.git) or press Enter to skip: "
if not "%REPO_URL%"=="" (
    git remote remove origin 2>nul
    git remote add origin %REPO_URL%
    echo [*] Remote origin set to %REPO_URL%
)

echo [*] Staging files...
git add .

echo [*] Creating commit...
git commit -m "Optimize Forwarding Bot for Heroku deployment"

echo [*] Pushing to main branch...
git push -u origin main

echo ==========================================================
echo Finished! If push failed, make sure your GitHub repo exists
echo and credentials are configured.
echo ==========================================================
pause
