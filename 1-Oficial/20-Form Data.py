# Form Data
from typing import Annotated
from fastapi import FastAPI, Form

app = FastAPI()

# Importa Form
@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}


# Define parámetros de Form
@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}


# Campos de formulario booleanos
@app.post("/preferences/")
async def update_preferences(subscribe: Annotated[bool, Form()] = False):
    return {"subscribe": subscribe}