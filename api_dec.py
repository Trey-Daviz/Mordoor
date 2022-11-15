import json
from fastapi import Request


def api(func):
    async def handler(request: Request) -> None:
        try:
            info = await request.body()
            print(info)
            info = info.decode("utf-8")
            info = json.loads(info)
            func_ret = func(info)
        except Exception as error:
            raise
        return func_ret

    return handler
