
import os
import time
from random import randint
from typing import Optional

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from names import get_full_name
from odmantic import AIOEngine
from odmantic import Field as field
from odmantic import Model
from pydantic import BaseModel, Field  # pylint: disable=no-name-in-module

from .env import env

engine = AIOEngine(client=AsyncIOMotorClient(env.DATABASE_URL))


class MetricsSchema(BaseModel):
    """The schema of the metrics."""

    latency: float = Field(
        ..., description="The time taken for the request to be processed by the server."
    )
    cpu_cycle: int = Field(
        ...,
        description="The number of CPU cycles taken for the request to be processed by the server.",
    )
    memory: int = Field(
        ...,
        description="The amount of memory taken for the request to be processed by the server.",
    )
    network_time: float = Field(
        ..., description="The time taken for the request to be processed by the server."
    )
    network_speed: float = Field(..., description="The network speed of the server.")
    requests_per_second: float = Field(
        ..., description="The number of requests processed by the server per second."
    )


class MetricsModel(Model):
    """The metrics stored in the database."""

    metrics: MetricsSchema = field(..., description="The schema of the metrics.")
    endpoint: str = field(..., description="The endpoint of the metrics.")
    method: str = field(..., description="The method of the metrics.")
    timestamp: float = field(
        default_factory=time.time, description="The timestamp of the metrics."
    )

    async def save(self):
        await engine.save(self)


class Dummy(Model):
    name: Optional[str] = field(default_factory=get_full_name)
    age: Optional[int] = field(default_factory=lambda: randint(0, 100))

    async def save(self):
        await engine.save(self)

    @classmethod
    async def all(cls):
        return await engine.find(cls)
