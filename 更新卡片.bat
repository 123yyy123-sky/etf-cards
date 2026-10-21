@echo off
chcp 65001 >nul
cd /d "%~dp0"
set PY="C:\Users\35313\.workbuddy\binaries\python\versions\3.13.12\python.exe"

echo === 1/4 从知识库抽取卡片 ===
%PY% build\extract.py
if errorlevel 1 goto err

echo.
echo === 2/4 生成单文件 App ===
%PY% build\build.py
if errorlevel 1 goto err

echo.
echo === 3/4 提交到本地仓库 ===
git add -A
git commit -m "更新卡片 %DATE% %TIME%"
if errorlevel 1 echo （没有变化，跳过提交）

echo.
echo === 4/4 推送到 GitHub ===
git push
if errorlevel 1 (
  echo.
  echo [!] 推送失败。本地已更新，云端还是旧的。
  echo     多半是网络或代理问题，网络好了再跑一次这个脚本即可。
  goto end
)

echo.
echo 完成 -^> 本地 %~dp0ETF知识卡.html
echo        云端 https://github.com/123yyy123-sky/etf-cards
goto end

:err
echo.
echo [!] 构建失败，没有提交，云端未改动。

:end
pause
