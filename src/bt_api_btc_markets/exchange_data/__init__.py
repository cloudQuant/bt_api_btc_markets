"""BTC Markets Exchange Data Configuration."""

from __future__ import annotations

from bt_api_base.containers.exchanges.exchange_data import ExchangeData


class BtcMarketsExchangeData(ExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "BTC_MARKETS"
        self.rest_url = "https://api.btcmarkets.net"
        self.wss_url = "wss://socket.btcmarkets.net/v3"
        self.kline_periods = {
            "1m": "1m",
            "1h": "1h",
            "1d": "1d",
        }
        self.legal_currency = ["AUD"]
        self.rest_paths = {}
        self.wss_paths = {}


class BtcMarketsExchangeDataSpot(BtcMarketsExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.asset_type = "spot"
