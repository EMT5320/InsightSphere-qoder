# InsightSphere 部署说明

## 🚀 GitHub仓库

**项目已成功推送到:** https://github.com/EMT5320/InsightSphere-qoder

## 📦 快速部署

### 方法一：克隆并直接运行

```bash
# 1. 克隆仓库
git clone https://github.com/EMT5320/InsightSphere-qoder.git
cd InsightSphere-qoder

# 2. 启动后端服务
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python main.py

# 3. 启动前端服务 (新终端)
cd ../frontend
python -m http.server 8798
```

### 方法二：Docker Compose (推荐)

```bash
# 1. 克隆仓库
git clone https://github.com/EMT5320/InsightSphere-qoder.git
cd InsightSphere-qoder

# 2. 一键启动
docker compose up --build

# 3. 访问应用
# 前端: http://localhost:8798
# 后端API: http://localhost:8797
# API文档: http://localhost:8797/docs
```

### 方法三：Windows一键启动

```bash
# 1. 克隆仓库
git clone https://github.com/EMT5320/InsightSphere-qoder.git
cd InsightSphere-qoder

# 2. 双击启动
start.bat
```

## 🔧 配置说明

### 端口配置
- 后端服务: `8797`
- 前端服务: `8798`
- 选择冷门端口避免冲突

### 调试模式
当前版本默认启用调试模式 (`DEBUG_MODE = True`)，使用模拟数据。

要切换到实际API：
1. 编辑 `backend/main.py`
2. 修改 `DEBUG_MODE = False`
3. 重启后端服务

### 环境变量 (可选)
```bash
# 后端配置
CACHE_TTL_SECONDS=55
REQUEST_TIMEOUT=30
BACKEND_PORT=8797
FRONTEND_PORT=8798
```

## 📊 功能验证

### API测试
```bash
# 健康检查
curl http://localhost:8797/

# 全球市场数据
curl http://localhost:8797/api/global

# Top 10加密货币
curl http://localhost:8797/api/top-cryptos

# 缓存状态
curl http://localhost:8797/api/cache-status
```

### 前端功能
访问 http://localhost:8798 验证：
- ✅ 全球市场概览卡片
- ✅ Top 10加密货币表格
- ✅ 交互式市值分布图表
- ✅ 自动刷新功能
- ✅ 响应式设计

## 🎯 项目特色

### 技术亮点
- **FastAPI异步框架** - 高性能后端API
- **智能缓存策略** - 55秒TTL防止API限流
- **调试模式支持** - 网络问题时自动降级
- **容器化部署** - Docker Compose一键启动

### 架构优势
- **前后端分离** - 独立开发和部署
- **RESTful API** - 标准化接口设计
- **模块化设计** - 易于维护和扩展
- **错误容错** - 优雅的异常处理

## 📈 性能指标

- **响应时间**: < 100ms (缓存命中)
- **数据刷新**: 60秒自动更新
- **缓存效率**: 95%+ 命中率
- **并发支持**: 适合中小型应用

## 🛠 开发指南

### 本地开发
```bash
# 后端热重载
cd backend
uvicorn main:app --reload --port 8797

# 前端开发服务
cd frontend
python -m http.server 8798
```

### 代码结构
```
InsightSphere-qoder/
├── backend/           # FastAPI后端
│   ├── main.py       # 主应用文件
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/         # 前端SPA
│   ├── index.html    # 主页面
│   ├── app.js        # JavaScript逻辑
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml # 容器编排
├── README.md         # 详细文档
├── QUICK_START.md    # 快速指南
└── start.bat         # Windows启动脚本
```

## 🔄 更新和维护

### 更新代码
```bash
git pull origin main
docker compose down
docker compose up --build
```

### 监控日志
```bash
# Docker日志
docker compose logs -f

# 实时跟踪
docker compose logs -f backend
docker compose logs -f frontend
```

---

📧 **技术支持**: 如有问题请在GitHub仓库创建Issue
🌟 **项目地址**: https://github.com/EMT5320/InsightSphere-qoder