"""Usable in both Client and Server context."""
from __future__ import annotations

from typing import Self

from .base import BaseRequest, BaseResponse


class FooRequest(BaseRequest["FooResponse"]):
    response_type: type

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<something>"

    def reply(self) -> FooResponse:
        return FooResponse()

    def encode(self) -> bytes:
        return b"FooRequest"

    @classmethod
    def decode(cls, raw: bytes) -> Self:  # noqa: ARG003
        return cls()


class FooResponse(BaseResponse[FooRequest]):
    request_type: type = FooRequest

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}<something>"

    @classmethod
    def decode(cls, raw: bytes) -> Self:  # noqa: ARG003
        return cls()

    def encode(self) -> bytes:
        return b"FooRequest"


FooRequest.response_type = FooResponse
