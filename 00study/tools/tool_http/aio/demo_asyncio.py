import asyncio
import sys

from fastapi import FastAPI, Request
import uvicorn


def get_event_loop() -> asyncio.AbstractEventLoop:
    """get event loop in runtime"""
    if sys.version_info >= (3, 7):
        return asyncio.get_running_loop()

    loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    if not loop.is_running():
        raise RuntimeError("no running event loop")
    return loop


class Demo(object):
    def __init__(self, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        else:
            loop = loop


class BadClient(object):
    def __init__(self) -> None:
        self._loop = asyncio.get_event_loop()

    async def fake_request(self) -> None:
        await self._loop.create_task(asyncio.sleep(1))
        return None


# app = FastAPI()
# client = BadClient()
#
#
# @app.get("/")
# async def demo() -> str:
#     await client.fake_request()
#     return "Hello World!"
#
#
# uvicorn.run(app)
# attached to a different loop

app = FastAPI()


@app.on_event("startup")
async def startup() -> None:
    app.client = BadClient()


@app.get("/")
async def demo(request: Request) -> str:
    await request.app.client.fake_request()
    return "Hello World!"


uvicorn.run(app)
