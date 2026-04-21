"""BTC Markets exchange plugin."""

from __future__ import annotations

from bt_api_base.plugins.protocol import PluginInfo
from bt_api_btc_markets.exchange_data import BtcMarketsExchangeDataSpot


class BtcMarketsPlugin:
    @staticmethod
    def get_plugin_info() -> PluginInfo:
        return PluginInfo(
            name="btc_markets",
            display_name="BTC Markets",
            version="0.1.0",
            supported_asset_types=["SPOT"],
        )

    @staticmethod
    def get_exchange_data(asset_type: str = "SPOT"):
        if asset_type == "SPOT":
            return BtcMarketsExchangeDataSpot()
        raise ValueError(f"Unsupported asset type: {asset_type}")
