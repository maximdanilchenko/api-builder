import json
from urllib.parse import parse_qs


class Request:

    def __init__(self, app, headers, method, path, query_string, **_):
        self.app = app
        self.headers = headers
        self.method = method
        self.path = path
        self.query_params = parse_qs(query_string.decode())
        self.path_params = None
        self.schema = None
        self.body = None
        self._json = None
        self._stream = None
        self._responded = False

    async def read(self):
        body = []
        more_body = True
        while more_body:
            chunk = await self._stream[0]()
            body.append(chunk['body'])
            more_body = chunk['more_body']
        self.body = b''.join(body)

    async def json(self, schema=None):
        if self._json:
            return self.json

        if not self.body:
            await self.read()

        if schema is None:
            schema = self.schema

        self._json = json.loads(self.body.decode())

        if schema is not None:
            self._json = schema.validate(self._json)

        return self._json

    async def respond(self, response):
        if not self._responded:
            await self._stream[1]({"type": "http.response.start",
                                   "status": response.status,
                                   "headers": response.headers})
            await self._stream[1]({"type": "http.response.body",
                                   "body": response.body,
                                   "more_body": False})
            self._responded = True
