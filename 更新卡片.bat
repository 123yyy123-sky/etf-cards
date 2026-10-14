@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PY="C:\Users\35313\.workbuddy\binaries\python\versions\3.13.12\python.exe"
echo === 1/2 从知识库抽取卡片 ===
%PY% build\extract.py
echo === 2/2 生成单文件 App ===
%PY% build\build.py
echo.
echo 完成 -^> F:\Ai\ETF知识卡\ETF知识卡.html
pause
