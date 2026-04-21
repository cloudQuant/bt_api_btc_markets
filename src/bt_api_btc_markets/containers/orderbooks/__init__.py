from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base._compat import Self
from bt_api_base.containers.orderbooks.orderbook import OrderBookData
from bt_api_base.functions.utils import from_dict_get_float


class BtcMarketsOrderBookData(OrderBookData):
    def __init__(
        self,
        orderbook_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(orderbook_info, has_been_json_encoded)
        self.exchange_name = "BTC_MARKETS"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.orderbook_data: dict[str, Any] | None = (
            orderbook_info if has_been_json_encoded and isinstance(orderbook_info, dict) else None
        )
        self.bids: list = []
        self.asks: list = []
        self.has_been_init_data = False

    def init_data(self) -> Self:
        if not self.has_been_json_encoded:
            self.orderbook_data = json.loads(self.orderbook_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.orderbook_data, dict):
            data = self.orderbook_data
            bid_list = data.get("bids", [])
            ask_list = data.get("asks", [])
            self.bids = [
                {"price": from_dict_get_float(b, "0"), "quantity": from_dict_get_float(b, "1")}
                for b in bid_list
                if isinstance(b, (list, tuple)) and len(b) >= 2
            ]
            self.asks = [
                {"price": from_dict_get_float(a, "0"), "quantity": from_dict_get_float(a, "1")}
                for a in ask_list
                if isinstance(a, (list, tuple)) and len(a) >= 2
            ]

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_symbol_name(self) -> str:
        return self.symbol_name

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_bids(self) -> list:
        return self.bids

    def get_asks(self) -> list:
        return self.asks


class BtcMarketsRequestOrderBookData(BtcMarketsOrderBookData):
    pass