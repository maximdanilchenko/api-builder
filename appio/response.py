from typing import Dict
from json import dumps


class Response:
    def __init__(
        self, json=None, *, status=200, headers: Dict[str, str] = None, body=b""
    ):
        if json and body:
            raise Exception()

        self.status = status

        if headers is None:
            self.headers = {}
        else:
            self.headers = headers

        if json:
            self.body = dumps(json).encode()
        else:
            self.body = body
