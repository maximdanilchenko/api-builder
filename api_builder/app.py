from typing import Optional
from api_builder.request import Request
from api_builder.routes import RoutesGroup, Route


class App:
    def __init__(self, routes: RoutesGroup = None):
        self.routes = routes
        self._prepared = False

    def find_route(self, method: str, path: str) -> (Optional[Route], dict):
        if self.routes is None:
            return None, {}
        for route in self.routes.routes:
            if method.upper() == route.method:
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
        route, path_params = app.find_route(method=scope["method"], path=scope["path"])
        self.request = Request(app=app, route=route, path_params=path_params, **scope)

    async def __call__(self, receive, send):
        await self.request(receive, send)
