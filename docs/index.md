# BTC_MARKETS Documentation

## English

Welcome to the BTC_MARKETS documentation for bt_api.

### Quick Start

```bash
pip install bt_api_btc_markets
```

```python
from bt_api_btc_markets import BtcMarketsApi
feed = BtcMarketsApi(api_key="your_key", secret="your_secret")
ticker = feed.get_ticker("BTCUSDT")
```

## 中文

欢迎使用 bt_api 的 BTC_MARKETS 文档。

### 快速开始

```bash
pip install bt_api_btc_markets
```

```python
from bt_api_btc_markets import BtcMarketsApi
feed = BtcMarketsApi(api_key="your_key", secret="your_secret")
ticker = feed.get_ticker("BTCUSDT")
```

## API Reference

See source code in `src/bt_api_btc_markets/` for detailed API documentation.
