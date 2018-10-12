from json import dumps


class Response:
    def __init__(self, json=None, *, status=200, headers=None, body=b""):
        if json and body:
            raise Exception

        self.status = status

        if headers is None:
            self.headers = []
        else:
            self.headers = headers

        if json:
            self.body = dumps(json).encode()
        else:
            self.body = body

        self._stream = None

    async def respond(self):
        await self._stream({"type": "http.response.start",
                            "status": self.status,
                            "headers": self.headers})
        await self._stream({"type": "http.response.body",
                            "body": self.body,
                            "more_body": False})
