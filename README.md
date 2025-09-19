# InsightSphere - 实时加密货币数据可视化仪表盘

## 📊 项目简介

InsightSphere 是一个实时、交互式的加密货币市场数据可视化仪表盘。它从 CoinGecko API 获取实时数据，通过现代化的Web界面以多种图表形式动态展示给用户，为加密货币投资者、分析师和交易者提供关键的市场洞察。

### 🎯 核心功能

- **实时数据更新**: 每60秒自动刷新市场数据
- **全球市场概览**: 显示总市值、24小时交易量、比特币市值占比等关键指标
- **Top 10 排行榜**: 实时展示市值排名前10的加密货币详细信息
- **交互式图表**: 市值分布饼图，支持悬停交互和详细信息展示
- **响应式设计**: 支持桌面和移动设备的优化显示
- **错误容错**: 健壮的错误处理和用户友好的错误提示

## 🛠 技术选型

### 后端技术栈
- **FastAPI**: 选择原因 - 现代、快速的Python Web框架，内置异步支持，自动API文档生成
- **httpx**: 异步HTTP客户端，用于高效调用外部API
- **uvicorn**: ASGI服务器，支持高并发和异步处理
- **自定义TTL缓存**: 内存级缓存解决方案，避免频繁调用CoinGecko API被限流

### 前端技术栈
- **Vanilla JavaScript**: 轻量级选择，无框架依赖，快速加载
- **Chart.js**: 功能强大的图表库，支持交互式可视化
- **CSS Grid + Flexbox**: 现代布局技术，实现响应式设计
- **Font Awesome**: 图标库，提升用户界面体验

### 部署技术
- **Docker + Docker Compose**: 容器化部署，确保环境一致性和可移植性
- **多容器架构**: 前后端分离，便于扩展和维护

### 技术选型理由

1. **FastAPI vs Flask/Django**: FastAPI提供更好的异步支持，内置API文档，更适合API服务
2. **Vanilla JS vs React/Vue**: 项目规模适中，避免框架复杂性，减少bundle大小
3. **内存缓存 vs Redis**: 单实例部署场景下，内存缓存更简单高效
4. **Chart.js vs D3.js**: Chart.js上手更容易，满足当前可视化需求

## 🚀 快速开始

### 环境要求

- Python 3.11+
- Docker 和 Docker Compose（推荐）
- 或者：Node.js 18+（用于前端本地开发）

### 方法一：Docker Compose 一键部署（推荐）

1. **克隆项目到本地**
   ```bash
   cd D:\Work\arena\web_demo\qoder
   ```

2. **构建并启动服务**
   ```bash
   docker compose up --build
   ```

3. **访问应用**
   - 前端界面: http://localhost:8798
   - 后端API: http://localhost:8797
   - API文档: http://localhost:8797/docs

4. **停止服务**
   ```bash
   docker compose down
   ```

### 方法二：本地开发环境

#### 后端设置

1. **创建虚拟环境**
   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # 或 source .venv/bin/activate  # Linux/Mac
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

3. **启动后端服务**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8797
   ```

#### 前端设置

1. **进入前端目录**
   ```bash
   cd frontend
   ```

2. **启动前端服务**
   ```bash
   python -m http.server 8798
   ```

## 📡 API 文档

### 端点列表

#### 1. 健康检查
```
GET /
```
返回服务状态信息

#### 2. 全球市场数据
```
GET /api/global
```
返回全球加密货币市场概览数据

**响应示例:**
```json
{
  "success": true,
  "data": {
    "total_market_cap_usd": 2150000000000,
    "total_volume_usd": 95000000000,
    "bitcoin_dominance": 42.5,
    "ethereum_dominance": 18.2,
    "active_cryptocurrencies": 8937,
    "markets": 742,
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

#### 3. Top 10 加密货币
```
GET /api/top-cryptos
```
返回市值排名前10的加密货币详细数据

**响应示例:**
```json
{
  "success": true,
  "data": [
    {
      "rank": 1,
      "id": "bitcoin",
      "symbol": "BTC",
      "name": "Bitcoin",
      "image": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
      "current_price": 43250.50,
      "market_cap": 847234567890,
      "price_change_percentage_24h": 2.45,
      "total_volume": 25000000000
    }
  ]
}
```

#### 4. 缓存状态（调试用）
```
GET /api/cache-status
```
返回当前缓存状态信息

## 🔧 配置说明

### 环境变量
目前应用使用默认配置，未来可通过环境变量自定义：

- `CACHE_TTL_SECONDS`: 缓存过期时间（默认: 55秒）
- `REQUEST_TIMEOUT`: API请求超时时间（默认: 10秒）
- `BACKEND_PORT`: 后端服务端口（默认: 8797）
- `FRONTEND_PORT`: 前端服务端口（默认: 8798）

### 端口配置
应用使用以下冷门端口避免冲突：
- 后端: `8797`
- 前端: `8798`

## 🏗 项目结构

```
qoder/
├── backend/                 # 后端服务
│   ├── main.py             # FastAPI应用主文件
│   ├── requirements.txt    # Python依赖
│   └── Dockerfile          # 后端Docker配置
├── frontend/               # 前端应用
│   ├── index.html         # 主页面
│   ├── app.js             # JavaScript应用逻辑
│   ├── package.json       # 前端项目配置
│   └── Dockerfile         # 前端Docker配置
├── docker-compose.yml     # Docker Compose配置
└── README.md             # 项目文档
```

## 🔐 安全考虑

- **API限流**: 实现缓存机制避免过度调用外部API
- **错误处理**: 统一错误响应格式，避免敏感信息泄露
- **CORS配置**: 生产环境需限制允许的域名
- **输入验证**: 对所有外部输入进行验证和清理

## 📈 性能优化

### 缓存策略
- **TTL缓存**: 55秒过期时间，平衡数据新鲜度和API限制
- **内存缓存**: 高速访问，适合单实例部署
- **定期清理**: 每5分钟清理过期缓存，避免内存泄漏

### 前端优化
- **CDN资源**: Chart.js和Font Awesome使用CDN加速
- **异步加载**: 并行获取多个API数据
- **错误恢复**: 网络错误时的自动重试机制

## 🚨 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   netstat -ano | findstr :8797  # 检查端口占用
   ```

2. **Docker构建失败**
   ```bash
   docker compose build --no-cache  # 清除缓存重新构建
   ```

3. **API连接失败**
   - 检查网络连接
   - 验证CoinGecko API是否可访问
   - 查看后端日志: `docker compose logs backend`

4. **前端无法连接后端**
   - 确认后端服务已启动
   - 检查防火墙设置
   - 验证CORS配置

### 日志查看
```bash
# 查看所有服务日志
docker compose logs

# 查看特定服务日志
docker compose logs backend
docker compose logs frontend

# 实时跟踪日志
docker compose logs -f
```

## 🔄 开发工作流

### 开发模式
```bash
# 后端热重载
cd backend
uvicorn main:app --reload

# 前端文件服务
cd frontend
python -m http.server 8798
```

### 生产部署
```bash
# 生产环境构建
docker compose -f docker-compose.yml up -d

# 更新部署
docker compose pull
docker compose up -d
```

## 📊 监控和日志

- **健康检查**: 内置健康检查端点
- **访问日志**: uvicorn自动记录请求日志
- **错误监控**: 结构化错误日志记录
- **性能指标**: 缓存命中率和响应时间追踪

## 🛣 roadmap

### v1.1 计划功能
- [ ] Redis缓存支持多实例部署
- [ ] 用户偏好设置（货币单位、刷新频率）
- [ ] 更多图表类型（线图、柱状图）
- [ ] 价格预警功能
- [ ] 数据导出功能

### v1.2 计划功能
- [ ] 用户认证和个人仪表盘
- [ ] 投资组合跟踪
- [ ] 技术分析指标
- [ ] 移动端PWA支持

## 📄 许可证

MIT License - 详见 LICENSE 文件

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📞 支持

如有问题或建议，请通过以下方式联系：
- 创建 GitHub Issue
- 邮件联系项目维护者

---

**InsightSphere** - 让加密货币市场数据触手可及 🚀