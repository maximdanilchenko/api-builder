from appio import App, routes
from appio.schema import fields, Schema
from appio.spec import create_spec
from appio.response import Response
from appio.request import Request


class Person(Schema):
    name = fields.String(default="Unknown")


async def hello(request: Request):
    person = await request.json()
    return Response({"hello": f"{person['name']}"})


async def what_time(request: Request):
    import time
    print(request.headers)
    print(request.path)
    print(request.method)
    print(request.query_params)
    print(request.path_params)
    return Response(f"{time.time()}")


def create_app():
    app = App()
    app.routes = routes.group([
        routes.post("/hello", hello, schema=Person),
        routes.get("/time/{when}", what_time),
        routes.group(prefix="/v1", routes=[
            routes.get("/grouped", what_time)
        ])
    ])
    create_spec(app)
    return app


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(create_app(), host="localhost", port=8765)
