from parse import compile


class Route:
    def __init__(self, method, path, handler, schema):
        self.method = method
        self.path = path
        self.handler = handler
        self.schema = schema
        self.compiled = compile(path)


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
