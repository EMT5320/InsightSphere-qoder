@echo off
echo ===============================
echo InsightSphere 停止脚本
echo ===============================
echo.

echo 停止InsightSphere服务...
docker compose down

if %errorlevel% equ 0 (
    echo.
    echo InsightSphere已成功停止
) else (
    echo.
    echo 停止过程中出现错误
)

echo.
pause