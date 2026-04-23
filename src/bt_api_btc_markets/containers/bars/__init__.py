from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base._compat import Self
from bt_api_base.containers.bars.bar import BarData
from bt_api_base.functions.utils import from_dict_get_float


class BtcMarketsBarData(BarData):
    def __init__(
        self,
        bar_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        period: str | None = None,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(bar_info, has_been_json_encoded)
        self.exchange_name = "BTC_MARKETS"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.period = period
        self.bar_data: list | None = (
            bar_info if has_been_json_encoded and isinstance(bar_info, list) else None
        )
        self.open_time: float | None = None
        self.open: float | None = None
        self.high: float | None = None
        self.low: float | None = None
        self.close: float | None = None
        self.volume: float | None = None
        self.has_been_init_data = False

    def init_data(self) -> Self:
        if not self.has_been_json_encoded:
            self.bar_data = json.loads(self.bar_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.bar_data, list) and len(self.bar_data) > 0:
            first = self.bar_data[0]
            if isinstance(first, dict):
                self.open_time = from_dict_get_float(first, "timestamp") or from_dict_get_float(
                    first,
                    "time",
                )
                self.open = from_dict_get_float(first, "open")
                self.high = from_dict_get_float(first, "high")
                self.low = from_dict_get_float(first, "low")
                self.close = from_dict_get_float(first, "close")
                self.volume = from_dict_get_float(first, "volume")
            elif isinstance(first, (list, tuple)) and len(first) >= 6:
                self.open_time = float(first[0])
                self.open = float(first[1])
                self.high = float(first[2])
                self.low = float(first[3])
                self.close = float(first[4])
                self.volume = float(first[5])

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_symbol_name(self) -> str:
        return self.symbol_name

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_open_time(self) -> float | None:
        return self.open_time

    def get_open(self) -> float | None:
        return self.open

    def get_high(self) -> float | None:
        return self.high

    def get_low(self) -> float | None:
        return self.low

    def get_close(self) -> float | None:
        return self.close

    def get_volume(self) -> float | None:
        return self.volume


class BtcMarketsRequestBarData(BtcMarketsBarData):
    pass
