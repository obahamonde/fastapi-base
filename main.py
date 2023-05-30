from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from lib.tests import StatefulBenchmark

app = FastAPI()

stateful = StatefulBenchmark()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/http")
async def http_endpoint():
    return await stateful.http()


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await stateful.websocket(ws)


@app.get("/database")
async def database_endpoint():
    return await stateful.test_db()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    allow_credentials=True,
    allow_origin_regex="*",
)
