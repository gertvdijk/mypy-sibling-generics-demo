# Python type-annotated 'sibling' classes

## What is this demo about?

Typed response types on sending a request awaiting response in a client
context – and vice-versa for a server context.
The main idea is that sending a request of Python object type A must return a Python
object of type that matches the request type A (or else raise an exception).

This way of typing allows for creating a much cleaner API.
Instead of having an unbounded number of `get_foo(self) -> FooResponse` and
`get_bar(self, params: dict[...]) -> BarResponse` methods for all the features *foo* and
*bar*, it allows for a much simpler API; just a single *generically typed* method
`get(self, request: Request[T]) -> T`.

The other benefit is that this 'communicator' class is decoupled from logic about
request/responses and only has to care about passing the messages.
Extending the features of the communicator would then only involve adding new
Request/Response class types and keep the communicator class itself untouched.

## Example / demo 🚀

```python
bar_response = MyClient().send_and_await_response(req=bar.BarRequest(drink="beer"))
# The response is fully revealed as bar.BarResponse on type-check time. 🎉
reveal_type(bar_response)
```

```
$ mypy foobar/client.py
foobar/client.py:63: note: Revealed type is "foobar.bar.BarResponse"
foobar/client.py:71: note: Revealed type is "foobar.foo.FooResponse"
Success: no issues found in 1 source file
```

Runtime test:

Client checks out.
```
$ python -m foobar.client
```

Similar (inverse) pattern for the server checks out too:

```
$ python -m foobar.server
```

A server that fails (deliberately!) at runtime to parse a request we don't have a
response that we can encode.

```
$ python -m foobar.server_expected_failure
[...]
  File "/.../foobar/server_expected_failure.py", line 13, in main_test_server
    server.MyServer().handle_incoming_request(
  File "/.../foobar/server.py", line 52, in handle_incoming_request
    self.send_response(response=response)
  File "/.../foobar/server.py", line 63, in send_response
    encoded_response = response.encode()
                       ^^^^^^^^^^^^^^^
AttributeError: 'BarResponse' object has no attribute 'encode'. Did you mean: 'decode'?
[...]
```

Mypy typing type error as designed (**feature!**) on that occassion that
would have prevented the runtime error:

```
$ mypy --strict foobar/server_expected_failure.py
foobar/server_expected_failure.py:13: error: Value of type variable "SCResp_t_co" of
"handle_incoming_request" of "MyServer" cannot be "BarResponse"  [type-var]
```

The `foobar` package in this repository contains pure Protocol-based classes and
do not strictly require subclassing or any form of 'registration'.
It means that any class that confirms to the protocol (in this case implementing
`encode`/`decode`/`get_request_type`/`get_response_type` methods).

## Thoughts & room for improvement 🤔

- Could the `base.py`/`client.py`/`server.py` objects be designed easier?
- Instead of a classmethod returning the response/request type, can we simply have a
  ClassVar `response_type`/`request_type` with the type as value on them?
  - ... which seems to be blocked by mypy issue [#5144][mypy-5144],
  - ... or would it be possible to eliminate that altogether and infer the sibling type
    from the type annotations?
- Can we have a better mypy error as to where the user of the API passes the
  incompatible type? E.g.
    ```diff
    -foobar/server_expected_failure.py:13: error: Value of type variable "SCResp_t_co" of "handle_incoming_request" of "MyServer" cannot be "BarResponse"  [type-var]
    +foobar/server_expected_failure.py:13: error: Value of type variable as keyword argument "request_type" in "handle_incoming_request" of "MyServer" cannot be "BarRequest" (class attribute "response_type" does not implement protocol "ServerContextResponse")  [type-var]
    ```

[mypy-5144]: https://github.com/python/mypy/issues/5144#issuecomment-1001222212
