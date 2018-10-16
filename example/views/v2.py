from api_builder.response import Response
from api_builder.request import Request


async def hello(request: Request):
    person = await request.json()
    return Response({"hello": f"{person['name']}"})


async def info(request: Request):
    return Response({"info": {
        "headers": dict(request.headers),
        "path": request.path,
        "method": request.method,
        "query_params": request.query_params,
        "path_params": request.path_params,
    }})


async def info_named(request: Request):
    print('Code before response!')
    response = Response({"name": request.path_params.get("name")})
    await request.respond(response)
    print('Code after response!')
