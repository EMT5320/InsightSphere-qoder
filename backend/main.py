"""
InsightSphere - 实时加密货币数据可视化仪表盘后端服务
使用FastAPI构建，提供CoinGecko API数据代理和缓存服务
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import asyncio
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging
import os

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="InsightSphere API",
    description="实时加密货币数据可视化仪表盘后端服务",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置参数
COINGECKO_BASE_URL = "https://api.coingecko.com/api/v3"
CACHE_TTL_SECONDS = 55  # 缓存时间略少于60秒，确保前端请求时数据是新的
REQUEST_TIMEOUT = 30  # 请求超时时间
DEBUG_MODE = True  # 调试模式，使用模拟数据

# 内存缓存
cache: Dict[str, Dict[str, Any]] = {}

class AsyncTTLCache:
    """异步TTL缓存类"""
    
    def __init__(self):
        self.cache = {}
    
    def get(self, key: str) -> Optional[Any]:
        """获取缓存数据"""
        if key in self.cache:
            data, expire_time = self.cache[key]
            if datetime.now() < expire_time:
                return data
            else:
                # 缓存过期，删除
                del self.cache[key]
        return None
    
    def set(self, key: str, value: Any, ttl_seconds: int = CACHE_TTL_SECONDS):
        """设置缓存数据"""
        expire_time = datetime.now() + timedelta(seconds=ttl_seconds)
        self.cache[key] = (value, expire_time)
    
    def clear_expired(self):
        """清理过期缓存"""
        current_time = datetime.now()
        expired_keys = [
            key for key, (_, expire_time) in self.cache.items()
            if current_time >= expire_time
        ]
        for key in expired_keys:
            del self.cache[key]

# 初始化缓存
app_cache = AsyncTTLCache()

def get_mock_global_data():
    """模拟全球市场数据"""
    return {
        "data": {
            "total_market_cap": {"usd": 2350000000000},
            "total_volume": {"usd": 98000000000},
            "market_cap_percentage": {"btc": 42.3, "eth": 18.7},
            "active_cryptocurrencies": 8947,
            "markets": 745,
            "updated_at": "2024-01-01T00:00:00Z"
        }
    }

def get_mock_crypto_data():
    """模拟Top 10加密货币数据"""
    return [
        {
            "id": "bitcoin",
            "symbol": "btc",
            "name": "Bitcoin",
            "image": "https://assets.coingecko.com/coins/images/1/large/bitcoin.png",
            "current_price": 43250.50,
            "market_cap": 847234567890,
            "market_cap_rank": 1,
            "price_change_percentage_24h": 2.45,
            "total_volume": 25000000000,
            "last_updated": "2024-01-01T00:00:00Z"
        },
        {
            "id": "ethereum",
            "symbol": "eth",
            "name": "Ethereum",
            "image": "https://assets.coingecko.com/coins/images/279/large/ethereum.png",
            "current_price": 2678.90,
            "market_cap": 321456789012,
            "market_cap_rank": 2,
            "price_change_percentage_24h": -1.23,
            "total_volume": 15000000000,
            "last_updated": "2024-01-01T00:00:00Z"
        },
        {
            "id": "tether",
            "symbol": "usdt",
            "name": "Tether",
            "image": "https://assets.coingecko.com/coins/images/325/large/Tether.png",
            "current_price": 1.00,
            "market_cap": 89123456789,
            "market_cap_rank": 3,
            "price_change_percentage_24h": 0.02,
            "total_volume": 28000000000,
            "last_updated": "2024-01-01T00:00:00Z"
        },
        {
            "id": "binancecoin",
            "symbol": "bnb",
            "name": "BNB",
            "image": "https://assets.coingecko.com/coins/images/825/large/bnb-icon2_2x.png",
            "current_price": 245.67,
            "market_cap": 37890123456,
            "market_cap_rank": 4,
            "price_change_percentage_24h": 3.21,
            "total_volume": 1200000000,
            "last_updated": "2024-01-01T00:00:00Z"
        },
        {
            "id": "solana",
            "symbol": "sol",
            "name": "Solana",
            "image": "https://assets.coingecko.com/coins/images/4128/large/solana.png",
            "current_price": 67.89,
            "market_cap": 28567891234,
            "market_cap_rank": 5,
            "price_change_percentage_24h": 5.67,
            "total_volume": 2100000000,
            "last_updated": "2024-01-01T00:00:00Z"
        },
        {
            "id": "ripple",
            "symbol": "xrp",
            "name": "XRP",
            "image": "https://assets.coingecko.com/coins/images/44/large/xrp-symbol-white-128.png",
            "current_price": 0.5234,
            "market_cap": 27890123456,
            "market_cap_rank": 6,
            "price_change_percentage_24h": -2.34,
            "total_volume": 1800000000,
            "last_updated": "2024-01-01T00:00:00Z"
        },
        {
            "id": "usd-coin",
            "symbol": "usdc",
            "name": "USD Coin",
            "image": "https://assets.coingecko.com/coins/images/6319/large/USD_Coin_icon.png",
            "current_price": 1.00,
            "market_cap": 25678901234,
            "market_cap_rank": 7,
            "price_change_percentage_24h": -0.01,
            "total_volume": 4200000000,
            "last_updated": "2024-01-01T00:00:00Z"
        },
        {
            "id": "cardano",
            "symbol": "ada",
            "name": "Cardano",
            "image": "https://assets.coingecko.com/coins/images/975/large/cardano.png",
            "current_price": 0.3789,
            "market_cap": 13456789012,
            "market_cap_rank": 8,
            "price_change_percentage_24h": 1.89,
            "total_volume": 890000000,
            "last_updated": "2024-01-01T00:00:00Z"
        },
        {
            "id": "avalanche-2",
            "symbol": "avax",
            "name": "Avalanche",
            "image": "https://assets.coingecko.com/coins/images/12559/large/Avalanche_Circle_RedWhite_Trans.png",
            "current_price": 23.45,
            "market_cap": 8901234567,
            "market_cap_rank": 9,
            "price_change_percentage_24h": 4.12,
            "total_volume": 650000000,
            "last_updated": "2024-01-01T00:00:00Z"
        },
        {
            "id": "dogecoin",
            "symbol": "doge",
            "name": "Dogecoin",
            "image": "https://assets.coingecko.com/coins/images/5/large/dogecoin.png",
            "current_price": 0.0789,
            "market_cap": 11234567890,
            "market_cap_rank": 10,
            "price_change_percentage_24h": -0.89,
            "total_volume": 1100000000,
            "last_updated": "2024-01-01T00:00:00Z"
        }
    ]

async def fetch_with_cache(url: str, cache_key: str) -> Dict[str, Any]:
    """带缓存的HTTP请求"""
    
    # 检查缓存
    cached_data = app_cache.get(cache_key)
    if cached_data:
        logger.info(f"Cache hit for {cache_key}")
        return cached_data
    
    # 缓存未命中，发起请求
    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
            logger.info(f"Fetching data from {url}")
            response = await client.get(url)
            response.raise_for_status()
            
            data = response.json()
            
            # 存入缓存
            app_cache.set(cache_key, data)
            logger.info(f"Data cached for {cache_key}")
            
            return data
            
    except httpx.TimeoutException:
        logger.error(f"Timeout when fetching {url}")
        raise HTTPException(status_code=504, detail="外部API请求超时")
    except httpx.HTTPStatusError as e:
        logger.error(f"HTTP error when fetching {url}: {e.response.status_code}")
        raise HTTPException(status_code=502, detail="外部API请求失败")
    except Exception as e:
        logger.error(f"Unexpected error when fetching {url}: {str(e)}")
        raise HTTPException(status_code=500, detail="服务器内部错误")

@app.get("/")
async def root():
    """健康检查端点"""
    return {
        "service": "InsightSphere API",
        "status": "running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/global")
async def get_global_market_data():
    """获取全球市场概览数据"""
    try:
        if DEBUG_MODE:
            # 使用模拟数据
            data = get_mock_global_data()
            logger.info("Using mock global data (DEBUG_MODE=True)")
        else:
            url = f"{COINGECKO_BASE_URL}/global"
            data = await fetch_with_cache(url, "global_market")
        
        # 提取关键数据
        global_data = data.get("data", {})
        
        return {
            "success": True,
            "data": {
                "total_market_cap_usd": global_data.get("total_market_cap", {}).get("usd", 0),
                "total_volume_usd": global_data.get("total_volume", {}).get("usd", 0),
                "bitcoin_dominance": global_data.get("market_cap_percentage", {}).get("btc", 0),
                "ethereum_dominance": global_data.get("market_cap_percentage", {}).get("eth", 0),
                "active_cryptocurrencies": global_data.get("active_cryptocurrencies", 0),
                "markets": global_data.get("markets", 0),
                "updated_at": global_data.get("updated_at", None)
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_global_market_data: {str(e)}")
        raise HTTPException(status_code=500, detail="获取全球市场数据失败")

@app.get("/api/top-cryptos")
async def get_top_cryptocurrencies():
    """获取市值排名前10的加密货币数据"""
    try:
        if DEBUG_MODE:
            # 使用模拟数据
            data = get_mock_crypto_data()
            logger.info("Using mock crypto data (DEBUG_MODE=True)")
        else:
            url = f"{COINGECKO_BASE_URL}/coins/markets"
            params = {
                "vs_currency": "usd",
                "order": "market_cap_desc",
                "per_page": 10,
                "page": 1,
                "sparkline": False,
                "price_change_percentage": "24h"
            }
            
            # 构建完整URL
            param_str = "&".join([f"{k}={v}" for k, v in params.items()])
            full_url = f"{url}?{param_str}"
            
            data = await fetch_with_cache(full_url, "top_cryptos")
        
        # 处理数据格式
        processed_data = []
        for i, coin in enumerate(data):
            processed_data.append({
                "rank": i + 1,
                "id": coin.get("id", ""),
                "symbol": coin.get("symbol", "").upper(),
                "name": coin.get("name", ""),
                "image": coin.get("image", ""),
                "current_price": coin.get("current_price", 0),
                "market_cap": coin.get("market_cap", 0),
                "market_cap_rank": coin.get("market_cap_rank", 0),
                "price_change_percentage_24h": coin.get("price_change_percentage_24h", 0),
                "total_volume": coin.get("total_volume", 0),
                "last_updated": coin.get("last_updated", None)
            })
        
        return {
            "success": True,
            "data": processed_data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_top_cryptocurrencies: {str(e)}")
        raise HTTPException(status_code=500, detail="获取加密货币排行数据失败")

@app.get("/api/cache-status")
async def get_cache_status():
    """获取缓存状态（用于调试）"""
    app_cache.clear_expired()  # 清理过期缓存
    
    cache_info = {}
    for key in app_cache.cache:
        _, expire_time = app_cache.cache[key]
        cache_info[key] = {
            "expires_at": expire_time.isoformat(),
            "expires_in_seconds": (expire_time - datetime.now()).total_seconds()
        }
    
    return {
        "success": True,
        "data": {
            "cache_count": len(app_cache.cache),
            "cache_details": cache_info
        }
    }

# 定期清理过期缓存的后台任务
@app.on_event("startup")
async def startup_event():
    """应用启动时的初始化"""
    logger.info("InsightSphere API starting up...")
    
    # 启动定期清理缓存的任务
    async def cleanup_cache():
        while True:
            await asyncio.sleep(300)  # 每5分钟清理一次
            app_cache.clear_expired()
            logger.info("Cache cleanup completed")
    
    asyncio.create_task(cleanup_cache())
    logger.info("InsightSphere API started successfully")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8797)  # 使用冷门端口8797