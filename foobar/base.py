from __future__ import annotations

from typing import Any, Protocol, Self, TypeVar


class SupportsEncode(Protocol):
    def encode(self) -> bytes:
        ...


class SupportsDecode(Protocol):
    @classmethod
    def decode(cls, raw: bytes) -> Self:
        ...


Req_t_co = TypeVar("Req_t_co", bound="BaseRequest[Any]", covariant=True)
Res_t_co = TypeVar("Res_t_co", bound="BaseResponse[Any]", covariant=True)


class BaseRequest(Protocol[Res_t_co]):
    response_type: type

    @classmethod
    def get_response_type(cls) -> type[Res_t_co]:
        return cls.response_type  # pyright: ignore[reportGeneralTypeIssues]


class BaseResponse(Protocol[Req_t_co]):
    request_type: type

    @classmethod
    def get_request_type(cls) -> type[Req_t_co]:
        return cls.request_type  # pyright: ignore[reportGeneralTypeIssues]
