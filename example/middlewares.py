from appio.request import Request


async def some_middleware(request: Request, handler):
    print("do something before handler")
    resp = await handler(request)
    print("do something after handler")
    return resp
