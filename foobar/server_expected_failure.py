from __future__ import annotations

from . import bar, server


def main_test_server() -> None:
    # mypy error expected here (A FEATURE OF THIS PACKAGE)!
    # Although bar.BarRequest can decode requests, its mapped response type lacks an
    # encode() method. Therefore also the request can only be used in client contexts.
    # At runtime it will crash like this (as prevented by type checker):
    #   AttributeError: 'BarResponse' object has no attribute 'encode'.
    server.MyServer().handle_incoming_request(
        request_encoded=b"beer",
        request_type=bar.BarRequest,  # <-- mypy/pyright failure expected
    )


if __name__ == "__main__":
    main_test_server()
