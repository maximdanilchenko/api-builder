# Appio

Python ASGI framework for building APIs 

_As for now it's in very early stage of development_

It's core/unique features are(will be):
- Routes are formed in groups. Group can include another groups and routes. So it is perfect for scaling and versioning.
- Middleware functions can be mounted not on the app, but on any group or route. So it adds flexibility to web app architecture. 
- Builtin validation and documentation engine. 


#### Example of using groups for api versioning:
```python
import uvicorn

from appio import App, Response
from appio.routes import group, get
    
async def hello_v1(request):
    user = request.path_params["user"]
    return Response(f"hello {user}")
    
async def hello_v2(request):
    user = request.path_params["user"]
    return Response(f"Hello {user}!")

api_routes = group(
    group(
        get("/hello/{user}", hello_v1), 
        prefix="/v1"
    ),
    group(
        get("/hello/{user}", hello_v2), 
        prefix="/v2"
        ),
)

app = App(routes=api_routes)

uvicorn.run(app)
```

#### Example of using validation engine:
```python
import uvicorn

from appio import App, Response
from appio.routes import group, get
from appio.schema import Schema, fields, validators

class User(Schema):
    name = fields.String(default="Unknown", allow_none=False)
    age = fields.Integer(validators=[validators.Range(min=18)])
    
async def hello(request):
    user = await request.json()
    return Response(f"hello {user[name]}")
    
api_routes = group(
    get("/hello/{user}", hello, schema=User),
)
app = App(routes=api_routes)

uvicorn.run(app)
```

#### Example of using middlewares in route groupes:
```python
async def some_middleware(request, handler):
    print("do something before handler")
    resp = await handler(request)
    print("do something after handler")
    return resp
    
    
api_v1 = group(
    get("/hello/{user}", hello),
    middlewares=[some_middleware],
)
```