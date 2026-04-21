"""Tests for BtcMarketsExchangeData container."""

from __future__ import annotations

from bt_api_btc_markets.exchange_data import BtcMarketsExchangeData


class TestBtcMarketsExchangeData:
    """Tests for BtcMarketsExchangeData."""

    def test_init(self):
        """Test initialization."""
        exchange = BtcMarketsExchangeData()

        assert exchange.exchange_name == "BTC_MARKETS"
