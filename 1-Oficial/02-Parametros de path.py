# Parámetros de Path

from fastapi import FastAPI
from enum import Enum

# CLASE ENUM
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

app = FastAPI()


# PARAMETROS DE PATH
@app.get("/items/{item_id}")
async def read_item(item_id):
    return {"item_id": item_id}


# PARAMETROS CON TIPOS
@app.get("/items2/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


# EL ORDEN IMPORTA
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# CON PATH CON MISMO NOMBRE SOLO SE TOMA EL PRIMERO
@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]


# VALORES PREDEFINIDOS
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# PARAMETROS DE PATH CONTENIENDO PATHS
# No fue comprendido del todo
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}