from typing import Optional
from appio.request import Request
from appio.routes import RoutesGroup, Route


class App:
    def __init__(self, routes_group: RoutesGroup=None):
        self.routes = routes_group

        self._prepared = False

    def find_route(self, path: str) -> (Optional[Route], dict):
        for route in self.routes.routes:
            parse_result = route.compiled.parse(path)
            if parse_result:
                return route, parse_result.named
        return None, {}

    def __call__(self, scope):
        return Connection(scope, self)


class Connection:
    def __init__(self, scope, app):

        if scope["type"] != "http":
            raise NotImplementedError()

        route, path_params = app.find_route(scope['path'])
        self.request = Request(app=app, route=route, path_params=path_params, **scope)

    async def __call__(self, receive, send):
        await self.request(receive, send)
