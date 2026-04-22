from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base._compat import Self
from bt_api_base.containers.accounts.account import AccountData
from bt_api_base.functions.utils import from_dict_get_float


class BtcMarketsAccountData(AccountData):
    def __init__(
        self,
        account_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(account_info, has_been_json_encoded)
        self.exchange_name = "BTC_MARKETS"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.account_data: dict[str, Any] | list | None = (
            account_info
            if has_been_json_encoded and isinstance(account_info, (dict, list))
            else None
        )
        self.balances: list = []
        self.has_been_init_data = False

    def init_data(self) -> Self:
        if not self.has_been_json_encoded:
            self.account_data = json.loads(self.account_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.account_data, list):
            self.balances = [
                {
                    "asset": from_dict_get_float(item, "asset"),
                    "available": from_dict_get_float(item, "available"),
                    "locked": from_dict_get_float(item, "locked"),
                }
                for item in self.account_data
                if isinstance(item, dict)
            ]
        elif isinstance(self.account_data, dict):
            self.balances = [self.account_data]

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_symbol_name(self) -> str:
        return self.symbol_name

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_balances(self) -> list:
        return self.balances


class BtcMarketsRequestAccountData(BtcMarketsAccountData):
    pass
