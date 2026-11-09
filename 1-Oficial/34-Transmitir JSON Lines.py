# Transmitir JSON Lines
from collections.abc import AsyncIterable, Iterable
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()


# TRANSMITIR JSONO LINES CON FASTAPI
# Introduccion
class Item(BaseModel):
    name: str
    description: str | None

items = [
    Item(name="Plumbus", description="A multi-purpose household device."),
    Item(name="Portal Gun", description="A portal opening device."),
    Item(name="Meeseeks Box", description="A box that summons a Meeseeks."),
]

@app.get("/items/stream")
async def stream_items() -> AsyncIterable[Item]:
    for item in items:
        yield item
# Code below omitted 👇

from collections.abc import AsyncIterable, Iterable
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None

items = [
    Item(name="Plumbus", description="A multi-purpose household device."),
    Item(name="Portal Gun", description="A portal opening device."),
    Item(name="Meeseeks Box", description="A box that summons a Meeseeks."),
]

@app.get("/items/stream")
async def stream_items() -> AsyncIterable[Item]:
    for item in items:
        yield item
# Code below omitted 👇


# path operation functions no-async
# Code above omitted 👆
@app.get("/items/stream-no-async")
def stream_items_no_async() -> Iterable[Item]:
    for item in items:
        yield item
# Code below omitted 👇


# Sin tipo de retorno
# Code above omitted 👆
@app.get("/items/stream-no-annotation")
async def stream_items_no_annotation():
    for item in items:
        yield item
# Code below omitted 👇