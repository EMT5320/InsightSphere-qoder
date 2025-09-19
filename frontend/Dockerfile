# 前端Dockerfile
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制前端文件
COPY . .

# 暴露端口
EXPOSE 8798

# 启动HTTP服务器
CMD ["python", "-m", "http.server", "8798"]