from __future__ import annotations

import base64
from typing import Any

from bt_api_btc_markets.feeds.live_btc_markets.request_base import BtcMarketsRequestData


def test_btc_markets_accepts_public_private_key_aliases(monkeypatch: Any) -> None:
    private_key = base64.b64encode(b"secret-key").decode("utf-8")
    request_data = BtcMarketsRequestData(public_key="public-key", private_key=private_key)
    monkeypatch.setattr(
        "bt_api_btc_markets.feeds.live_btc_markets.request_base.time.time", lambda: 1700000000.0
    )

    headers = request_data._get_headers("GET", "/v3/accounts", None, None)

    assert request_data.api_key == "public-key"
    assert request_data.api_secret == private_key
    assert headers["BM-AUTH-APIKEY"] == "public-key"
    assert headers["BM-AUTH-SIGNATURE"]
