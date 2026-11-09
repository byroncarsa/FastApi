# Codificador compatible con JSON
from datetime import datetime
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


# USANDO EL JSONABLE_ENCODER
fake_db = {}

class Item(BaseModel):
    title: str
    timestamp: datetime
    description: str | None = None

app = FastAPI()

@app.put("/items/{id}")
def update_item(id: str, item: Item):
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data