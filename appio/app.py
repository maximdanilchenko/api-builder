from appio.request import Request
from appio.response import Response
from appio.routes import RoutesGroup


class App:
    def __init__(self, routes_group: RoutesGroup=None):
        self.routes = routes_group

        self._prepared = False

    def __call__(self, scope):
        return Connection(scope, self)


class Connection:
    def __init__(self, scope, app):

        if scope["type"] != "http":
            raise NotImplementedError()

        self.app = app
        self.request = Request(app=app, **scope)

    def find_route(self):
        for route in self.app.routes.routes:
            parse_result = route.compiled.parse(self.request.path)
            if parse_result:
                self.request.path_params = parse_result.named
                return route

    async def __call__(self, receive, send):
        self.request._stream = (receive, send)

        route = self.find_route()
        if route:
            response = await route.handler(self.request)
        else:
            response = Response("Not Found", status=404)

        await self.request.respond(response)

