import json
from typing import List, Dict, Tuple
from urllib.parse import parse_qs
from functools import partial

from multidict import CIMultiDict

from api_builder.response import Response


class Request:
    def __init__(
        self, app, headers, method, path, query_string, route, path_params, **_
    ):
        self.app = app
        self.row_headers = headers
        self.headers = self._decode_headers(headers)
        self.method = method
        self.path = path
        self.query_params = parse_qs(query_string.decode())
        self.path_params = path_params
        self._route = route
        self.body = None
        self._json = None
        self._receive = None
        self._send = None
        self._responded = False

    @staticmethod
    def _decode_headers(row_headers: List[Tuple[bytes, bytes]]) -> CIMultiDict:
        # TODO: write headers parser instead of using multidict.CIMultiDict
        return CIMultiDict(
            (k.decode("latin-1"), v.decode("latin-1")) for k, v in row_headers
        )

    @staticmethod
    def _encode_headers(headers: Dict[str, str]) -> List[Tuple[bytes, bytes]]:
        return [(k.encode(), v.encode()) for k, v in headers.items()]

    async def read(self):
        body = []
        more_body = True
        while more_body:
            chunk = await self._receive()
            body.append(chunk["body"])
            more_body = chunk["more_body"]
        self.body = b"".join(body)

    async def json(self, schema=None):
        if self._json is not None:
            return self.json

        if not self.body:
            await self.read()

        if schema is None:
            schema = self._route.schema

        self._json = json.loads(self.body.decode())

        if schema is not None:
            self._json = schema.validate(self._json)

        return self._json

    async def respond(self, response):
        if not self._responded:
            await self._send(
                {
                    "type": "http.response.start",
                    "status": response.status,
                    "headers": self._encode_headers(response.headers),
                }
            )
            await self._send(
                {
                    "type": "http.response.body",
                    "body": response.body,
                    "more_body": False,
                }
            )
            self._responded = True

    async def __call__(self, receive, send):

        self._receive = receive
        self._send = send

        if self._route:
            handler = self._route.handler
            for m in self._route.middlewares:
                handler = partial(m, handler=handler)
            response = await handler(self)
        else:
            response = Response("Not Found", status=404)

        await self.respond(response)
