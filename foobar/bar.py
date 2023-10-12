"""Only usable in Client context."""
from __future__ import annotations

from typing import Self

import attrs

from .base import BaseRequest, BaseResponse


@attrs.define(auto_attribs=False, slots=False, kw_only=True)
class BarRequest(BaseRequest["BarResponse"]):
    response_type: type
    drink: str = attrs.field()

    def __repr__(self) -> str:
        return f"BarRequest, ordered drink: {self.drink}."

    def reply(self) -> BarResponse:
        match self.drink:
            case "beer as string":
                return BarResponse(bill=5.95)
            case "many":
                return BarResponse(bill=50.0)
            case _:
                return BarResponse(bill=0.0)

    @classmethod
    def decode(cls, raw: bytes) -> Self:
        return cls(drink=raw.decode("utf-8") + " as string")

    def encode(self) -> bytes:
        return self.drink.encode()


@attrs.define(auto_attribs=False, slots=False, kw_only=True)
class BarResponse(BaseResponse[BarRequest]):
    request_type: type = BarRequest
    bill: float = attrs.field()

    def __repr__(self) -> str:
        return f"Price of the bill is {self.bill}."

    @classmethod
    def decode(cls, raw: bytes) -> Self:
        price = float(raw.decode())
        return cls(bill=price)

    # Omitted encode() method on purpose for demonstrating BarRequest can't be used in
    # server context as validated on type checking time.
    # def encode(self) -> bytes:


BarRequest.response_type = BarResponse


BarRequest.response_type = BarResponse
