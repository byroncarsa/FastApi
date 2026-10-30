# Parámetros de Cookie
from typing import Annotated
from fastapi import Cookie, FastAPI

app = FastAPI()

# Importar Cookie
@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}


# Importar Cookie
@app.get("/items/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}


