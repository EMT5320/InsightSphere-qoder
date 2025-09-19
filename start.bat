@echo off
echo ===============================
echo InsightSphere 启动脚本
echo ===============================
echo.

echo 检查Docker是否运行...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: Docker未安装或未启动
    echo 请先安装并启动Docker Desktop
    pause
    exit /b 1
)

echo 检查Docker Compose是否可用...
docker compose version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: Docker Compose不可用
    pause
    exit /b 1
)

echo.
echo 停止现有容器（如果存在）...
docker compose down

echo.
echo 构建并启动InsightSphere...
docker compose up --build -d

if %errorlevel% equ 0 (
    echo.
    echo ===============================
    echo InsightSphere 启动成功！
    echo ===============================
    echo 前端地址: http://localhost:8798
    echo 后端API: http://localhost:8797
    echo API文档: http://localhost:8797/docs
    echo.
    echo 按任意键查看服务日志...
    pause >nul
    docker compose logs -f
) else (
    echo.
    echo 启动失败，请检查错误信息
    pause
)