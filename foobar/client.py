from __future__ import annotations

from typing import TYPE_CHECKING, Any, Protocol, TypeVar, reveal_type

from . import bar, foo
from .base import BaseRequest, BaseResponse, SupportsDecode, SupportsEncode

CCReq_t_co = TypeVar("CCReq_t_co", bound="ClientContextRequest[Any]", covariant=True)
CCResp_t_co = TypeVar("CCResp_t_co", bound="ClientContextResponse[Any]", covariant=True)


class ClientContextRequest(
    SupportsEncode,
    BaseRequest[CCResp_t_co],
    Protocol[CCResp_t_co],
):
    """
    Generic Request type that can be used in a client context.

    Type-checking aware protocol class to ensure:
    - classmethod encode() exists to send a request over the wire, and
    - the mapped response class has an instance method decode() to make sense of the
      encoded response (bytes/serialized) received.
    """


class ClientContextResponse(
    SupportsDecode,
    BaseResponse[CCReq_t_co],
    Protocol[CCReq_t_co],
):
    """
    Generic Response type that can be used in a client context.

    Type-checking aware protocol class to ensure:
    - classmethod decode() exists that returns itself, and
    - the mapped request class has an instance method encode().
    """


DUMMY_DATA = b"1.95"


class MyClient:
    def send_and_await_response(
        self, *, req: ClientContextRequest[CCResp_t_co]
    ) -> CCResp_t_co:
        to_send = req.encode()
        print(f"Client will send: {to_send!r}")
        response_type = req.get_response_type()
        ret = response_type.decode(DUMMY_DATA)
        print(f"Response from server: {ret}")

        return ret


def main_test_client() -> None:
    bar_response = MyClient().send_and_await_response(req=bar.BarRequest(drink="beer"))
    if TYPE_CHECKING:
        # The response is fully revealed as bar.BarResponse on type-check time. 🎉
        reveal_type(bar_response)
    # And checks out at runtime as well...
    assert type(bar_response) == bar.BarResponse
    print(f"{bar_response.bill!r} ({type(bar_response.bill)})")

    foo_response = MyClient().send_and_await_response(req=foo.FooRequest())
    if TYPE_CHECKING:
        # The response is fully revealed as foo.FooResponse on type-check time. 🎉
        reveal_type(foo_response)
    # And checks out at runtime as well...
    assert type(foo_response) == foo.FooResponse


if __name__ == "__main__":
    main_test_client()
