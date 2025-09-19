/**
 * InsightSphere - 前端JavaScript应用
 * 负责数据获取、处理和可视化
 */

class InsightSphere {
    constructor() {
        this.apiBase = 'http://localhost:8797/api';
        this.chart = null;
        this.refreshInterval = null;
        this.isLoading = false;
        
        this.init();
    }

    async init() {
        console.log('InsightSphere 初始化中...');
        await this.loadAllData();
        this.startAutoRefresh();
    }

    async loadAllData() {
        if (this.isLoading) return;
        
        this.isLoading = true;
        this.updateRefreshButton(true);

        try {
            // 并行加载所有数据
            const [globalData, cryptoData] = await Promise.all([
                this.fetchGlobalData(),
                this.fetchTopCryptos()
            ]);

            // 更新UI
            this.updateGlobalMetrics(globalData);
            this.updateMarketStats(globalData);
            this.updateCryptoTable(cryptoData);
            this.updateChart(cryptoData);
            
            this.updateLastUpdated();
            console.log('数据加载完成');
            
        } catch (error) {
            console.error('数据加载失败:', error);
            this.showError('数据加载失败，请检查网络连接或稍后重试');
        } finally {
            this.isLoading = false;
            this.updateRefreshButton(false);
        }
    }

    async fetchGlobalData() {
        try {
            const response = await fetch(`${this.apiBase}/global`);
            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.message || '获取全球数据失败');
            }
            
            return result.data;
        } catch (error) {
            console.error('获取全球数据失败:', error);
            throw error;
        }
    }

    async fetchTopCryptos() {
        try {
            const response = await fetch(`${this.apiBase}/top-cryptos`);
            const result = await response.json();
            
            if (!result.success) {
                throw new Error(result.message || '获取加密货币数据失败');
            }
            
            return result.data;
        } catch (error) {
            console.error('获取加密货币数据失败:', error);
            throw error;
        }
    }

    updateGlobalMetrics(data) {
        const container = document.getElementById('global-metrics');
        
        container.innerHTML = `
            <div class="metric">
                <span class="metric-label">总市值</span>
                <span class="metric-value">${this.formatCurrency(data.total_market_cap_usd)}</span>
            </div>
            <div class="metric">
                <span class="metric-label">24h 总交易量</span>
                <span class="metric-value">${this.formatCurrency(data.total_volume_usd)}</span>
            </div>
            <div class="metric">
                <span class="metric-label">比特币占比</span>
                <span class="metric-value">${data.bitcoin_dominance.toFixed(1)}%</span>
            </div>
            <div class="metric">
                <span class="metric-label">以太坊占比</span>
                <span class="metric-value">${data.ethereum_dominance.toFixed(1)}%</span>
            </div>
        `;
    }

    updateMarketStats(data) {
        const container = document.getElementById('market-stats');
        
        container.innerHTML = `
            <div class="metric">
                <span class="metric-label">活跃加密货币</span>
                <span class="metric-value">${this.formatNumber(data.active_cryptocurrencies)}</span>
            </div>
            <div class="metric">
                <span class="metric-label">交易所数量</span>
                <span class="metric-value">${this.formatNumber(data.markets)}</span>
            </div>
            <div class="metric">
                <span class="metric-label">其他占比</span>
                <span class="metric-value">${(100 - data.bitcoin_dominance - data.ethereum_dominance).toFixed(1)}%</span>
            </div>
            <div class="metric">
                <span class="metric-label">数据状态</span>
                <span class="metric-value" style="color: #48bb78;">
                    <i class="fas fa-check-circle"></i> 实时
                </span>
            </div>
        `;
    }

    updateCryptoTable(cryptos) {
        const tbody = document.getElementById('crypto-table-body');
        
        tbody.innerHTML = cryptos.map(crypto => `
            <tr>
                <td><strong>#${crypto.rank}</strong></td>
                <td>
                    <div class="crypto-info">
                        <img src="${crypto.image}" alt="${crypto.name}" class="crypto-logo" 
                             onerror="this.src='data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzIiIGhlaWdodD0iMzIiIHZpZXdCb3g9IjAgMCAzMiAzMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iMTYiIGN5PSIxNiIgcj0iMTYiIGZpbGw9IiM3QzhCOEIiLz4KPHN2ZyB4PSI4IiB5PSI4IiB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSI+CjxwYXRoIGQ9Ik04IDJMMTQgOEw4IDE0TDIgOEw4IDJaIiBmaWxsPSJ3aGl0ZSIvPgo8L3N2Zz4KPC9zdmc+'">
                        <div class="crypto-name">
                            <span class="crypto-symbol">${crypto.symbol}</span>
                            <span class="crypto-full-name">${crypto.name}</span>
                        </div>
                    </div>
                </td>
                <td><strong>$${this.formatPrice(crypto.current_price)}</strong></td>
                <td>
                    <span class="price-change ${crypto.price_change_percentage_24h >= 0 ? 'positive' : 'negative'}">
                        ${crypto.price_change_percentage_24h >= 0 ? '+' : ''}${crypto.price_change_percentage_24h.toFixed(2)}%
                    </span>
                </td>
                <td>${this.formatCurrency(crypto.market_cap)}</td>
                <td>${this.formatCurrency(crypto.total_volume)}</td>
            </tr>
        `).join('');
    }

    updateChart(cryptos) {
        const ctx = document.getElementById('marketCapChart').getContext('2d');
        
        // 销毁之前的图表
        if (this.chart) {
            this.chart.destroy();
        }

        // 准备图表数据
        const labels = cryptos.map(crypto => crypto.symbol);
        const data = cryptos.map(crypto => crypto.market_cap);
        const colors = this.generateColors(cryptos.length);

        this.chart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: colors,
                    borderWidth: 2,
                    borderColor: '#ffffff'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: {
                            usePointStyle: true,
                            padding: 20,
                            font: {
                                size: 12
                            }
                        }
                    },
                    tooltip: {
                        callbacks: {
                            label: (context) => {
                                const crypto = cryptos[context.dataIndex];
                                const percentage = ((crypto.market_cap / cryptos.reduce((sum, c) => sum + c.market_cap, 0)) * 100).toFixed(1);
                                return `${crypto.symbol}: $${this.formatNumber(crypto.market_cap)} (${percentage}%)`;
                            }
                        }
                    }
                },
                interaction: {
                    intersect: false,
                    mode: 'index'
                }
            }
        });
    }

    generateColors(count) {
        const colors = [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF',
            '#FF9F40', '#FF6384', '#C9CBCF', '#4BC0C0', '#FF6384'
        ];
        return colors.slice(0, count);
    }

    formatCurrency(value) {
        if (value >= 1e12) {
            return '$' + (value / 1e12).toFixed(2) + 'T';
        } else if (value >= 1e9) {
            return '$' + (value / 1e9).toFixed(2) + 'B';
        } else if (value >= 1e6) {
            return '$' + (value / 1e6).toFixed(2) + 'M';
        } else if (value >= 1e3) {
            return '$' + (value / 1e3).toFixed(2) + 'K';
        } else {
            return '$' + value.toFixed(2);
        }
    }

    formatPrice(price) {
        if (price >= 1) {
            return price.toLocaleString('en-US', {
                minimumFractionDigits: 2,
                maximumFractionDigits: 2
            });
        } else {
            return price.toFixed(6);
        }
    }

    formatNumber(value) {
        return value.toLocaleString('en-US');
    }

    updateLastUpdated() {
        const element = document.getElementById('last-updated');
        const now = new Date();
        element.innerHTML = `
            <span class="status-indicator"></span>
            最后更新: ${now.toLocaleString('zh-CN')} | 下次更新: ${new Date(now.getTime() + 60000).toLocaleTimeString('zh-CN')}
        `;
    }

    startAutoRefresh() {
        // 清除之前的定时器
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
        }

        // 每60秒刷新一次
        this.refreshInterval = setInterval(() => {
            console.log('自动刷新数据...');
            this.loadAllData();
        }, 60000);

        console.log('自动刷新已启动 (60秒间隔)');
    }

    updateRefreshButton(loading) {
        const button = document.querySelector('.refresh-btn');
        const icon = button.querySelector('i');
        
        if (loading) {
            button.disabled = true;
            icon.className = 'fas fa-spinner fa-spin';
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> 刷新中...';
        } else {
            button.disabled = false;
            icon.className = 'fas fa-sync-alt';
            button.innerHTML = '<i class="fas fa-sync-alt"></i> 刷新数据';
        }
    }

    showError(message) {
        // 显示错误信息
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error';
        errorDiv.innerHTML = `
            <i class="fas fa-exclamation-triangle"></i> ${message}
            <button onclick="this.parentElement.remove()" style="float: right; background: none; border: none; color: inherit; cursor: pointer;">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        document.querySelector('.container').insertBefore(errorDiv, document.querySelector('.dashboard'));
        
        // 5秒后自动移除
        setTimeout(() => {
            if (errorDiv.parentElement) {
                errorDiv.remove();
            }
        }, 5000);
    }
}

// 全局函数，供HTML调用
function loadAllData() {
    if (window.app) {
        window.app.loadAllData();
    }
}

// 页面加载完成后初始化应用
document.addEventListener('DOMContentLoaded', () => {
    window.app = new InsightSphere();
});

// 错误处理
window.addEventListener('error', (event) => {
    console.error('JavaScript错误:', event.error);
});

// 网络状态监控
window.addEventListener('online', () => {
    console.log('网络已连接');
    if (window.app) {
        window.app.loadAllData();
    }
});

window.addEventListener('offline', () => {
    console.log('网络已断开');
    if (window.app) {
        window.app.showError('网络连接已断开，数据可能不是最新的');
    }
});

console.log('InsightSphere JavaScript模块已加载');