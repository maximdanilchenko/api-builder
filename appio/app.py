from appio.request import Request
from appio.response import Response


class App:
    def __init__(self, routes=None):

        if routes is None:
            self.routes = []
        else:
            self.routes = routes
        self._prepared = False
        self._routes = None

    def __call__(self, scope):
        return AsgiProxy(scope, self)


class AsgiProxy:
    def __init__(self, scope, app):
        if scope["type"] != "http":
            raise NotImplementedError()
        self.app = app
        self.request = Request(app=app, **scope)

    async def __call__(self, receive, send):
        self.request._stream = receive

        for route in self.app.routes:
            parse_result = route.compiled.parse(self.request.path)
            if parse_result:
                self.request.path_params = parse_result.named
                response = await route.handler(self.request)
                break
        else:
            response = Response("Not Found", status=404)

        response._stream = send

        await response.respond()

