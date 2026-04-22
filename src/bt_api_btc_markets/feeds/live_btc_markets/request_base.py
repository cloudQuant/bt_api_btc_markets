from __future__ import annotations

import base64
import hashlib
import hmac
import json
import time
from typing import Any

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.feeds.capability import Capability
from bt_api_base.feeds.feed import Feed
from bt_api_base.feeds.http_client import HttpClient

from bt_api_btc_markets.exchange_data import BtcMarketsExchangeDataSpot


class BtcMarketsRequestData(Feed):
    @classmethod
    def _capabilities(cls) -> set[Capability]:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.GET_EXCHANGE_INFO,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
        }

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.data_queue = data_queue
        self.exchange_name = kwargs.get("exchange_name", "BTC_MARKETS___SPOT")
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self._params = BtcMarketsExchangeDataSpot()
        self.api_key = kwargs.get("public_key") or kwargs.get("api_key")
        self.api_secret = kwargs.get("private_key") or kwargs.get("api_secret")
        self._http_client = HttpClient(venue=self.exchange_name, timeout=10)

    def _generate_signature(self, method: str, path: str, nonce: str, body: str = "") -> str:
        secret_b64 = self.api_secret
        if not secret_b64:
            return ""
        secret = base64.b64decode(secret_b64)
        auth = method + path + nonce
        if method == "POST" and body:
            auth += body
        signature = hmac.new(secret, auth.encode(), hashlib.sha512).digest()
        return base64.b64encode(signature).decode()

    def _get_headers(
        self, method: str, request_path: str, params: dict = None, body: dict = None,
    ) -> dict:
        nonce = str(int(time.time() * 1000))
        body_str = ""
        if method == "POST" and body:
            body_str = json.dumps(body, separators=(",", ":"))
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "BM-AUTH-APIKEY": self.api_key or "",
            "BM-AUTH-TIMESTAMP": nonce,
            "BM-AUTH-SIGNATURE": self._generate_signature(method, request_path, nonce, body_str),
        }
        return headers

    def request(
        self, path: str, params=None, body=None, extra_data=None, timeout=10,
    ) -> RequestData:
        method = path.split()[0] if " " in path else "GET"
        request_path = path.split()[1] if " " in path else path
        headers = self._get_headers(method, request_path, params, body)
        try:
            url = self._params.rest_url + request_path
            if method == "GET" and params:
                query = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
                url = url + "?" + query
            response = self._http_client.request(
                method=method,
                url=url,
                headers=headers,
                json_data=body if method == "POST" else None,
                params=None,
            )
            return RequestData(response, extra_data or {})
        except Exception as e:
            self.logger.error(f"Request failed: {e}")
            raise

    async def async_request(
        self, path: str, params=None, body=None, extra_data=None, timeout=5,
    ) -> RequestData:
        method = path.split()[0] if " " in path else "GET"
        request_path = path.split()[1] if " " in path else path
        headers = self._get_headers(method, request_path, params, body)
        try:
            url = self._params.rest_url + request_path
            if method == "GET" and params:
                query = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
                url = url + "?" + query
            response = await self._http_client.async_request(
                method=method,
                url=url,
                headers=headers,
                json_data=body if method == "POST" else None,
                params=None,
            )
            return RequestData(response, extra_data or {})
        except Exception as e:
            self.async_logger.error(f"Async request failed: {e}")
            raise

    def async_callback(self, future: Any) -> None:
        try:
            result = future.result()
            if result is not None:
                self.push_data_to_queue(result)
        except Exception as e:
            self.async_logger.error(f"Async callback error: {e}")

    def push_data_to_queue(self, data: Any) -> None:
        if self.data_queue is not None:
            self.data_queue.put(data)

    def connect(self) -> None:
        pass

    def disconnect(self) -> None:
        super().disconnect()

    def is_connected(self) -> bool:
        return True
