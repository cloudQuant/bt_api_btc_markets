"""Registry registration for BTC Markets exchange."""

from __future__ import annotations

from bt_api_base.registry import ExchangeRegistry
from bt_api_btc_markets.plugin import BtcMarketsPlugin
from bt_api_btc_markets.feeds.live_btc_markets.spot import BtcMarketsRequestDataSpot


def register_btc_markets():
    plugin = BtcMarketsPlugin()
    info = plugin.get_plugin_info()
    exchange_data = plugin.get_exchange_data("SPOT")
    ExchangeRegistry.register(
        exchange_name="BTC_MARKETS___SPOT",
        exchange_data=exchange_data,
        feed_class=BtcMarketsRequestDataSpot,
        plugin_info=info,
    )


__all__ = ["register_btc_markets"]
