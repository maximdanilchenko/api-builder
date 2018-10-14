from appio.routes import group, get, post

from .views import v1, v2
from .schemas import Person
from .middlewares import some_middleware

api_routes = group(
    group(
        post("/hello", v1.hello, schema=Person),
        get("/info", v1.info),
        prefix="/v1",
    ),
    group(
        post("/hello", v2.hello, schema=Person),
        get("/info", v2.info),
        get("/info/{name}", v2.info_named),
        prefix="/v2",
        middlewares=[some_middleware]
    ),
)
