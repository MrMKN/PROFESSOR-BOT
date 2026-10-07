@echo off
title Push Mr.Guardian_bot to GitHub
cd /d "%~dp0"

echo ==========================================================
echo       Pushing Mr.Guardian_bot to GitHub (Heroku Ready)
echo ==========================================================
echo.

:: Ensure git identity is configured
git config user.name "Unknown993"
git config user.email "Unknown993@users.noreply.github.com"

:: Display current remote
git remote get-url origin 2>nul
if %errorlevel% neq 0 (
    echo [*] No remote origin detected.
    set /p REPO_URL="Enter your GitHub repository URL (e.g. https://github.com/USERNAME/REPO.git): "
    if not "%REPO_URL%"=="" (
        git remote add origin %REPO_URL%
    )
) else (
    echo.
    set /p CHANGE_URL="Press ENTER to keep current remote or paste a NEW GitHub repository URL: "
    if not "%CHANGE_URL%"=="" (
        git remote remove origin 2>nul
        git remote add origin %CHANGE_URL%
        echo [*] Remote origin updated.
    )
)

echo.
echo [*] Staging all files...
git add -A

echo [*] Committing latest changes...
git commit -m "Deploy: Update to Mr.Guardian Forwarding Bot optimized for Heroku" 2>nul

echo.
echo [*] Pushing branch 'main' to GitHub origin...
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo [!] Standard push encountered an issue.
    echo [!] If the remote repository has a different history, you can force push.
    set /p FORCE_CHOICE="Do you want to force push to overwrite the remote branch? (y/n): "
    if /i "%FORCE_CHOICE%"=="y" (
        git push -u origin main --force
    )
)

echo.
echo ==========================================================
echo  Done! Your repository is ready for Heroku deployment.
echo ==========================================================
pause
