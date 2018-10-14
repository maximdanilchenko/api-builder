from typing import Union
from parse import compile


class RoutesGroup:
    def __init__(self, prefix, routes):
        self.prefix = prefix
        self.routes = self.flatten(routes)

    def flatten(self, routes):
        # TODO: check that all routes are unique within one method
        flatten_routes = []
        for r in routes:
            if isinstance(r, RoutesGroup):
                flatten_routes.extend(r.routes)
            elif isinstance(r, Route):
                r.compiled = compile(self.prefix + r.path)
                flatten_routes.append(r)
            else:
                raise Exception()
        return flatten_routes


class Route:
    def __init__(self, method, path, handler, schema):
        self.method = method
        self.path = path
        self.handler = handler
        self.schema = schema
        self.compiled = None


def group(*routes: Union[Route, RoutesGroup], prefix: str="", middlewares=None):
    if not routes:
        raise Exception()
    return RoutesGroup(prefix, routes)


def route(method, path, handler, schema=None):
    return Route(method, path, handler, schema)


def get(path, handler, schema=None):
    return Route('GET', path, handler, schema)


def put(path, handler, schema=None):
    return Route('PUT', path, handler, schema)


def post(path, handler, schema=None):
    return Route('POST', path, handler, schema)


def delete(path, handler, schema=None):
    return Route('DELETE', path, handler, schema)


def patch(path, handler, schema=None):
    return Route('PATCH', path, handler, schema)
