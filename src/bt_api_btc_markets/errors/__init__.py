"""BTC Markets exchange errors."""

from __future__ import annotations

from bt_api_base.error import ErrorTranslator, UnifiedErrorCode


class BtcMarketsErrorTranslator(ErrorTranslator):
    @staticmethod
    def translate(error_code: int | str | None, response: dict | None = None) -> UnifiedErrorCode:
        if response is None:
            response = {}
        message = str(response.get("message", ""))
        error_msg = str(response.get("errorMsg", ""))
        code = str(error_code) if error_code is not None else ""

        if code == "0" or not code:
            return UnifiedErrorCode.SUCCESS

        if "insufficient" in message.lower() or "insufficient" in error_msg.lower():
            return UnifiedErrorCode.INSUFFICIENT_BALANCE
        if "not_found" in message.lower() or "not found" in error_msg.lower():
            return UnifiedErrorCode.ORDER_NOT_FOUND
        if "cancel" in message.lower() or "cancel" in error_msg.lower():
            return UnifiedErrorCode.ORDER_ALREADY_CANCELLED

        return UnifiedErrorCode.UNKNOWN_ERROR
