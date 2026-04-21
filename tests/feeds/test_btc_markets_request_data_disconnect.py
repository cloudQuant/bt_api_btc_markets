from __future__ import annotations

from unittest.mock import MagicMock

from bt_api_btc_markets.feeds.live_btc_markets.request_base import BtcMarketsRequestData


def test_btc_markets_disconnect_closes_http_client() -> None:
    request_data = BtcMarketsRequestData()
    request_data._http_client.close = MagicMock()

    request_data.disconnect()

    request_data._http_client.close.assert_called_once_with()
