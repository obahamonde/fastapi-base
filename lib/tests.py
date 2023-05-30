import asyncio
import json
from typing import Protocol

from fastapi import Response, WebSocket
from httpx import AsyncClient as Session  # pylint: disable=import-error

from .db import Dummy
from .env import env
from .metrics import metrics_stateful, metrics_stateless

session = Session()


async def test_get(i: int):
    return (await session.get(env.HTTP_URL + str(i))).json()


async def test_ws(i: int, ws: WebSocket):
    await ws.send_json({"id": i**i})


class Benchmark(Protocol):
    async def http(self) -> Response:
        """Http benchmark"""
        ...

    async def websocket(self, ws: WebSocket) -> Response:
        """Websocket benchmark"""
        ...

    async def test_db(self) -> Response:
        """Database benchmark"""
        ...


class StatefulBenchmark(Benchmark):
    """Benchmark that stores metrics in a database"""

    @metrics_stateful
    async def http(self):
        data = await asyncio.gather(*[test_get(i) for i in range(200)])
        return Response(
            status_code=200, content=json.dumps(data), media_type="application/json"
        )

    @metrics_stateful
    async def websocket(self, ws: WebSocket):
        data = await asyncio.gather(*[test_ws(i, ws) for i in range(10000)])
        return Response(
            status_code=200, content=json.dumps(data), media_type="application/json"
        )

    @metrics_stateful
    async def test_db(self):
        await asyncio.gather(*[Dummy().save() for i in range(50)])
        data = await Dummy.all()
        return Response(
            status_code=200,
            content=json.dumps([json.loads(i.json()) for i in data]),
            media_type="application/json",
        )


class StatelessBenchmark(Benchmark):
    """Benchmark that doesn't store metrics in a database"""

    @metrics_stateless
    async def http(self):
        data = await asyncio.gather(*[test_get(i) for i in range(1000)])
        return Response(
            status_code=200, content=json.dumps(data), media_type="application/json"
        )

    @metrics_stateless
    async def websocket(self, ws: WebSocket):
        data = await asyncio.gather(*[test_ws(i, ws) for i in range(10000)])
        return Response(
            status_code=200, content=json.dumps(data), media_type="application/json"
        )

    @metrics_stateless
    async def test_db(self):
        await asyncio.gather(*[Dummy().save() for i in range(100)])
        data = await Dummy.all()
        return Response(
            status_code=200,
            content=json.dumps([json.loads(i.json()) for i in data]),
            media_type="application/json",
        )
