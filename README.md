# BTC Markets Exchange Plugin for bt_api

## English | [中文](#中文)

---

## Overview

**BTC Markets** is one of Australia's longest-running cryptocurrency exchanges, operating since 2013. Based in Melbourne, it provides a secure platform for trading a wide variety of cryptocurrencies with AUD (Australian Dollar) trading pairs. BTC Markets is known for its robust security, regulatory compliance, and reliable service for Australian crypto investors.

This package provides the **BTC Markets exchange plugin for bt_api**, offering a unified interface for interacting with BTC Markets exchange through the [bt_api](https://github.com/cloudQuant/bt_api_py) framework.

### Key Features

- **REST API Integration**: Full access to BTC Markets' REST endpoints for market data and trading
- **Synchronous & Asynchronous**: Supports both sync and async request patterns
- **Unified Interface**: Integrates seamlessly with bt_api's `BtApi` class
- **AUD Trading Pairs**: Native support for AUD-quoted cryptocurrency pairs
- **HMAC-SHA512 Authentication**: Secure API key authentication with Base64 encoding

### Authentication

BTC Markets uses **HMAC-SHA512** signature authentication with Base64 encoding. The signature is computed as:

```
signature = Base64(HMAC-SHA512(secret, method + path + nonce + body))
```

Where:
- `method`: HTTP method (GET, POST, DELETE)
- `path`: The API path (e.g., `/v3/orders`)
- `nonce`: Unix timestamp in milliseconds
- `body`: Request body (empty string for GET/DELETE requests)

Required headers:
- `BM-AUTH-APIKEY`: Your API key
- `BM-AUTH-TIMESTAMP`: Unix timestamp in milliseconds
- `BM-AUTH-SIGNATURE`: Base64-encoded HMAC-SHA512 signature

### API Endpoint

| Environment | REST URL | WebSocket URL |
|------------|----------|---------------|
| Production | `https://api.btcmarkets.net` | `wss://socket.btcmarkets.net/v3` |

### Supported Operations

| Category | Operations | Status |
|----------|------------|--------|
| **Market Data** | Ticker, OrderBook, Klines/Candles | ✅ Supported |
| **Trading** | Place Order, Cancel Order, Query Order, Open Orders | ✅ Supported |
| **Account** | Balance, Account Info, Trading Fees | ✅ Supported |
| **Exchange Info** | Markets, Symbols | ✅ Supported |

### Supported Trading Pairs

BTC Markets supports trading with AUD as the quote currency. Common trading pairs include:

| Symbol | Description |
|--------|-------------|
| BTC-AUD | Bitcoin / Australian Dollar |
| ETH-AUD | Ethereum / Australian Dollar |
| XRP-AUD | Ripple / Australian Dollar |
| SOL-AUD | Solana / Australian Dollar |
| ADA-AUD | Cardano / Australian Dollar |
| DOGE-AUD | Dogecoin / Australian Dollar |

---

## Installation

### From PyPI (Recommended)

```bash
pip install bt_api_btc_markets
```

### From Source

```bash
git clone https://github.com/cloudQuant/bt_api_btc_markets
cd bt_api_btc_markets
pip install -e .
```

### Requirements

- Python 3.9 or higher
- bt_api_base >= 0.15
- Valid BTC Markets API key and secret

---

## Quick Start

### Initialize with BtApi

```python
from bt_api_py import BtApi

# Initialize with BTC Markets exchange
exchange_config = {
    "BTC_MARKETS___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_api_secret",
    }
}

api = BtApi(exchange_kwargs=exchange_config)

# Get ticker data
ticker = api.get_tick("BTC_MARKETS___SPOT", "BTC-AUD")
print(ticker)
```

### Direct Usage

```python
from bt_api_btc_markets.feeds.live_btc_markets.spot import BtcMarketsRequestDataSpot

# Initialize the feed directly
feed = BtcMarketsRequestDataSpot(
    api_key="your_api_key",
    secret="your_api_secret"
)

# Get ticker
ticker = feed.get_tick("BTC-AUD")
print(ticker)

# Get order book
depth = feed.get_depth("BTC-AUD", count=20)
print(depth)

# Get klines
klines = feed.get_kline("BTC-AUD", period="1h", count=100)
print(klines)
```

### Trading

```python
# Place a limit order
order = feed.make_order(
    symbol="BTC-AUD",
    volume=0.001,
    price=50000,
    order_type="Limit",  # Limit, Market, Stop, StopLimit
    offset="buy"  # buy (Bid) or sell (Ask)
)
print(order)

# Cancel order
result = feed.cancel_order("BTC-AUD", order_id="your_order_id")
print(result)

# Query order
order_info = feed.query_order("BTC-AUD", order_id="your_order_id")
print(order_info)
```

### Account Operations

```python
# Get account (trading fees)
account = feed.get_account()
print(account)

# Get balance
balance = feed.get_balance()
print(balance)

# Get open orders
open_orders = feed.get_open_orders()
print(open_orders)

# Get open orders for specific market
open_orders = feed.get_open_orders(symbol="BTC-AUD")
print(open_orders)
```

---

## API Reference

### Market Data

#### Get Ticker

```python
ticker = feed.get_tick("BTC-AUD")
```

#### Get Order Book

```python
depth = feed.get_depth("BTC-AUD", count=20)
```

#### Get Klines/Candles

```python
# Supported periods: 1m, 1h, 1d
klines = feed.get_kline("BTC-AUD", period="1h", count=100)
```

### Trading

#### Place Order

```python
# Limit order
order = feed.make_order(
    symbol="BTC-AUD",
    volume=0.01,
    price=50000,
    order_type="Limit",
    offset="buy"  # buy (Bid) or sell (Ask)
)

# Market order
order = feed.make_order(
    symbol="BTC-AUD",
    volume=0.01,
    price=0,  # price is ignored for market orders
    order_type="Market",
    offset="buy"
)
```

#### Cancel Order

```python
result = feed.cancel_order("BTC-AUD", order_id="your_order_id")
```

#### Query Order

```python
order_info = feed.query_order("BTC-AUD", order_id="your_order_id")
```

### Account

#### Get Balance

```python
balance = feed.get_balance()
```

#### Get Account Info (Trading Fees)

```python
account = feed.get_account()
```

#### Get Open Orders

```python
# All open orders
orders = feed.get_open_orders()

# Specific market
orders = feed.get_open_orders(symbol="BTC-AUD")
```

---

## Architecture

```
bt_api_btc_markets/
├── src/bt_api_btc_markets/        # Source code
│   ├── exchange_data/              # Exchange configuration and metadata
│   │   └── __init__.py           # BtcMarketsExchangeData, BtcMarketsExchangeDataSpot
│   ├── feeds/                     # API feeds
│   │   └── live_btc_markets/    # Live trading feed
│   │       ├── request_base.py    # Base class with HMAC auth
│   │       └── spot.py          # Spot trading implementation
│   ├── containers/                # Data containers
│   │   ├── tickers/             # Ticker containers
│   │   ├── orderbooks/        # OrderBook containers
│   │   ├── bars/               # K线 containers
│   │   ├── orders/             # Order containers
│   │   ├── accounts/          # Account containers
│   │   └── balances/          # Balance containers
│   ├── errors/                 # Error definitions
│   └── plugin.py             # Plugin registration
├── tests/                        # Unit tests
├── docs/                       # Documentation
├── pyproject.toml             # Package configuration
└── README.md                  # This file
```

---

## Error Handling

BTC Markets API errors are translated to standard bt_api exceptions. The plugin handles:

- **Authentication errors**: Invalid API key or signature
- **Permission errors**: Insufficient permissions for the operation
- **Rate limit errors**: Too many requests
- **Parameter errors**: Invalid request parameters

---

## Rate Limits

BTC Markets implements rate limiting on their API. The plugin includes built-in rate limiting to stay within acceptable bounds.

---

## Online Documentation

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-btc-markets.readthedocs.io/ |
| Chinese Docs | https://bt-api-btc-markets.readthedocs.io/zh/latest/ |
| GitHub Repository | https://github.com/cloudQuant/bt_api_btc_markets |
| Issue Tracker | https://github.com/cloudQuant/bt_api_btc_markets/issues |
| BTC Markets API Docs | https://api.btcmarkets.net/doc/v3 |

---

## License

MIT License - see [LICENSE](LICENSE) for details.

---

## Support

- Report bugs via [GitHub Issues](https://github.com/cloudQuant/bt_api_btc_markets/issues)
- Email: yunjinqi@gmail.com

---

## Changelog

### v0.1.0

- Initial release
- REST API support for spot trading
- HMAC-SHA512 authentication with Base64 encoding
- Support for AUD trading pairs
- Support for ticker, depth, klines, trading, balance operations

---

# 中文

---

## 概述

**BTC Markets** 是澳大利亚运行时间最长的加密货币交易所之一，自2013年开始运营。总部位于墨尔本，它为用户提供了一个安全的平台，可交易多种加密货币，主要以 AUD（澳大利亚元）交易对进行交易。BTC Markets 以其强大的安全性、监管合规性和为澳大利亚加密货币投资者提供的可靠服务而闻名。

本包为 [bt_api](https://github.com/cloudQuant/bt_api_py) 框架提供 **BTC Markets 交易所插件**，通过统一接口与 BTC Markets 交易所进行交互。

### 核心功能

- **REST API 集成**：全面访问 BTC Markets 的市场数据和交易 REST 端点
- **同步与异步**：支持同步和异步请求模式
- **统一接口**：与 bt_api 的 `BtApi` 类无缝集成
- **AUD 交易对**：原生支持 AUD 报价的加密货币交易对
- **HMAC-SHA512 认证**：采用 Base64 编码的安全 API 密钥认证

### 认证方式

BTC Markets 使用 **HMAC-SHA512** 签名认证，结合 Base64 编码。签名计算方式：

```
signature = Base64(HMAC-SHA512(secret, method + path + nonce + body))
```

其中：
- `method`：HTTP 方法（GET、POST、DELETE）
- `path`：API 路径（如 `/v3/orders`）
- `nonce`：Unix 时间戳（毫秒）
- `body`：请求体（GET/DELETE 请求为空字符串）

必需的请求头：
- `BM-AUTH-APIKEY`：您的 API 密钥
- `BM-AUTH-TIMESTAMP`：Unix 时间戳（毫秒）
- `BM-AUTH-SIGNATURE`：Base64 编码的 HMAC-SHA512 签名

### API 端点

| 环境 | REST URL | WebSocket URL |
|------|----------|---------------|
| 生产环境 | `https://api.btcmarkets.net` | `wss://socket.btcmarkets.net/v3` |

### 支持的操作

| 类别 | 操作 | 状态 |
|------|------|------|
| **市场数据** | 行情、订单簿、K线 | ✅ 已支持 |
| **交易** | 下单、撤单、查询订单、开放订单 | ✅ 已支持 |
| **账户** | 余额、账户信息、交易费用 | ✅ 已支持 |
| **交易所信息** | 市场、交易对 | ✅ 已支持 |

### 支持的交易对

BTC Markets 支持以 AUD 作为报价货币进行交易。常见交易对包括：

| 交易对 | 描述 |
|--------|------|
| BTC-AUD | 比特币 / 澳大利亚元 |
| ETH-AUD | 以太坊 / 澳大利亚元 |
| XRP-AUD | Ripple / 澳大利亚元 |
| SOL-AUD | Solana / 澳大利亚元 |
| ADA-AUD | 卡尔达诺 / 澳大利亚元 |
| DOGE-AUD | 狗狗币 / 澳大利亚元 |

---

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install bt_api_btc_markets
```

### 从源码安装

```bash
git clone https://github.com/cloudQuant/bt_api_btc_markets
cd bt_api_btc_markets
pip install -e .
```

### 系统要求

- Python 3.9 或更高版本
- bt_api_base >= 0.15
- 有效的 BTC Markets API 密钥和密钥

---

## 快速开始

### 使用 BtApi 初始化

```python
from bt_api_py import BtApi

# 使用 BTC Markets 交易所初始化
exchange_config = {
    "BTC_MARKETS___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_api_secret",
    }
}

api = BtApi(exchange_kwargs=exchange_config)

# 获取行情数据
ticker = api.get_tick("BTC_MARKETS___SPOT", "BTC-AUD")
print(ticker)
```

### 直接使用

```python
from bt_api_btc_markets.feeds.live_btc_markets.spot import BtcMarketsRequestDataSpot

# 直接初始化 feed
feed = BtcMarketsRequestDataSpot(
    api_key="your_api_key",
    secret="your_api_secret"
)

# 获取行情
ticker = feed.get_tick("BTC-AUD")
print(ticker)

# 获取订单簿
depth = feed.get_depth("BTC-AUD", count=20)
print(depth)

# 获取 K 线
klines = feed.get_kline("BTC-AUD", period="1h", count=100)
print(klines)
```

### 交易

```python
# 下限价单
order = feed.make_order(
    symbol="BTC-AUD",
    volume=0.001,
    price=50000,
    order_type="Limit",  # Limit, Market, Stop, StopLimit
    offset="buy"  # buy (Bid) 或 sell (Ask)
)
print(order)

# 撤单
result = feed.cancel_order("BTC-AUD", order_id="your_order_id")
print(result)

# 查询订单
order_info = feed.query_order("BTC-AUD", order_id="your_order_id")
print(order_info)
```

### 账户操作

```python
# 获取账户（交易费用）
account = feed.get_account()
print(account)

# 获取余额
balance = feed.get_balance()
print(balance)

# 获取开放订单
open_orders = feed.get_open_orders()
print(open_orders)

# 获取特定市场的开放订单
open_orders = feed.get_open_orders(symbol="BTC-AUD")
print(open_orders)
```

---

## API 参考

### 市场数据

#### 获取行情

```python
ticker = feed.get_tick("BTC-AUD")
```

#### 获取订单簿

```python
depth = feed.get_depth("BTC-AUD", count=20)
```

#### 获取 K 线

```python
# 支持的周期：1m, 1h, 1d
klines = feed.get_kline("BTC-AUD", period="1h", count=100)
```

### 交易

#### 下单

```python
# 限价单
order = feed.make_order(
    symbol="BTC-AUD",
    volume=0.01,
    price=50000,
    order_type="Limit",
    offset="buy"  # buy (Bid) 或 sell (Ask)
)

# 市价单
order = feed.make_order(
    symbol="BTC-AUD",
    volume=0.01,
    price=0,  # 市价单不需要价格
    order_type="Market",
    offset="buy"
)
```

#### 撤单

```python
result = feed.cancel_order("BTC-AUD", order_id="your_order_id")
```

#### 查询订单

```python
order_info = feed.query_order("BTC-AUD", order_id="your_order_id")
```

### 账户

#### 获取余额

```python
balance = feed.get_balance()
```

#### 获取账户信息（交易费用）

```python
account = feed.get_account()
```

#### 获取开放订单

```python
# 所有开放订单
orders = feed.get_open_orders()

# 特定市场
orders = feed.get_open_orders(symbol="BTC-AUD")
```

---

## 架构

```
bt_api_btc_markets/
├── src/bt_api_btc_markets/        # 源代码
│   ├── exchange_data/              # 交易所配置和元数据
│   │   └── __init__.py           # BtcMarketsExchangeData, BtcMarketsExchangeDataSpot
│   ├── feeds/                     # API feeds
│   │   └── live_btc_markets/    # 实时交易 feed
│   │       ├── request_base.py    # 带有 HMAC 认证的基类
│   │       └── spot.py          # 现货交易实现
│   ├── containers/                # 数据容器
│   │   ├── tickers/             # 行情容器
│   │   ├── orderbooks/        # 订单簿容器
│   │   ├── bars/               # K线容器
│   │   ├── orders/             # 订单容器
│   │   ├── accounts/          # 账户容器
│   │   └── balances/          # 余额容器
│   ├── errors/                 # 错误定义
│   └── plugin.py             # 插件注册
├── tests/                        # 单元测试
├── docs/                       # 文档
├── pyproject.toml             # 包配置
└── README.md                  # 本文件
```

---

## 错误处理

BTC Markets API 错误会转换为标准的 bt_api 异常。插件处理：

- **认证错误**：API 密钥或签名无效
- **权限错误**：操作权限不足
- **频率限制错误**：请求过于频繁
- **参数错误**：请求参数无效

---

## 频率限制

BTC Markets 在其 API 上实施了频率限制。插件内置了频率限制以保持在可接受的范围内。

---

## 在线文档

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-btc-markets.readthedocs.io/ |
| 中文文档 | https://bt-api-btc-markets.readthedocs.io/zh/latest/ |
| GitHub 仓库 | https://github.com/cloudQuant/bt_api_btc_markets |
| 问题反馈 | https://github.com/cloudQuant/bt_api_btc_markets/issues |
| BTC Markets API 文档 | https://api.btcmarkets.net/doc/v3 |

---

## 许可证

MIT 许可证 - 详见 [LICENSE](LICENSE)。

---

## 技术支持

- 通过 [GitHub Issues](https://github.com/cloudQuant/bt_api_btc_markets/issues) 反馈问题
- 邮箱: yunjinqi@gmail.com

---

## 更新日志

### v0.1.0

- 初始版本发布
- 支持现货交易的 REST API
- HMAC-SHA512 认证（Base64 编码）
- 支持 AUD 交易对
- 支持行情、订单簿、K线、交易、余额操作