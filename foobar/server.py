from __future__ import annotations

from typing import Any, Protocol, TypeVar

from . import foo
from .base import BaseRequest, BaseResponse, SupportsDecode, SupportsEncode

SCReq_t_co = TypeVar("SCReq_t_co", bound="ServerContextRequest[Any]", covariant=True)
SCResp_t_co = TypeVar("SCResp_t_co", bound="ServerContextResponse[Any]", covariant=True)


class ServerContextRequest(
    SupportsDecode, BaseRequest[SCResp_t_co], Protocol[SCResp_t_co]
):
    """
    Generic Request type that can be used in a server context.

    Type-checking aware protocol class to ensure:
    - classmethod decode() exists that returns itself, and
    - classmethod deply() exists that can build a response of type response class, and
    - the mapped response class has an instance method encode() to put it on the wire.
    """

    def reply(self) -> SCResp_t_co:
        ...


class ServerContextResponse(
    SupportsEncode, BaseResponse[SCReq_t_co], Protocol[SCReq_t_co]
):
    """
    Generic Response type that can be used in a server context.

    Type-checking aware protocol class to ensure:
    - instance method encode() exists, and
    - the mapped request class has a class method method decode().
    """


class MyServer:
    def handle_incoming_request(
        self,
        *,
        request_encoded: bytes,
        request_type: type[ServerContextRequest[SCResp_t_co]],
    ) -> None:
        request = request_type.decode(request_encoded)
        response = self.handle_decoded_request(req=request)
        print(f"will send {response}")
        self.send_response(response=response)

    def handle_decoded_request(
        self, *, req: ServerContextRequest[SCResp_t_co]
    ) -> SCResp_t_co:
        print(f"Received request from client: {req!r}")
        response_type = req.get_response_type()
        print(f"Will build a response: {response_type}")
        return req.reply()

    def send_response(self, *, response: ServerContextResponse[SCReq_t_co]) -> None:
        encoded_response = response.encode()
        print(f"will send encoded response back to the client... {encoded_response!r}")


def main_test_server() -> None:
    MyServer().handle_incoming_request(
        request_encoded=b"foo request data", request_type=foo.FooRequest
    )


if __name__ == "__main__":
    main_test_server()
