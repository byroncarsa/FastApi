# Modelos de Formulario
from typing import Annotated, Literal
from fastapi import FastAPI, Form, UploadFile
from pydantic import BaseModel

app = FastAPI()


# Modelos de Pydantic para Formularios
class FormData(BaseModel):
    username: str
    password: str


@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data


# Prohíbe Campos de Formulario Extra
class FormData(BaseModel):
    username: str
    password: str
    model_config = {"extra": "forbid"}


@app.post("/login/")
async def login(data: Annotated[FormData, Form()]):
    return data


# Combina Modelos de Formulario
class Profile(BaseModel):
    name: str


class Preferences(BaseModel):
    tags: list[str] = []


@app.post("/profiles/")
async def create_profile(
    profile: Annotated[Profile, Form()],
    preferences: Annotated[Preferences, Form()],
    token: Annotated[str, Form()],
):
    return {"profile": profile, "preferences": preferences, "token": token}


# Modelos de Formulario Opcionales
class Profile(BaseModel):
    name: str
    age: int


@app.post("/profiles/")
async def create_profile(
    token: Annotated[str, Form()],
    profile: Annotated[Profile | None, Form()] = None,
):
    return {"token": token, "profile": profile}


# Uniones Opcionales de Modelos de Formulario
class Person(BaseModel):
    kind: Literal["person"]
    name: str


class Company(BaseModel):
    kind: Literal["company"]
    company_name: str


@app.post("/contacts/")
async def create_contact(
    contact: Annotated[Person | Company | None, Form(discriminator="kind")] = None,
):
    return contact



# Combina Uniones de Modelos de Formulario
class Person(BaseModel):
    contact_type: Literal["person"]
    name: str


class Company(BaseModel):
    contact_type: Literal["company"]
    company_name: str


class Email(BaseModel):
    notification_type: Literal["email"]
    email: str


class SMS(BaseModel):
    notification_type: Literal["sms"]
    phone: str


@app.post("/contacts/")
async def create_contact(
    contact: Annotated[Person | Company, Form(discriminator="contact_type")],
    token: Annotated[str, Form()],
    notification: Annotated[
        Email | SMS | None, Form(discriminator="notification_type")
    ] = None,
):
    return {"contact": contact, "notification": notification, "token": token}

# Modelos de Formulario y Archivos
class Profile(BaseModel):
    name: str

@app.post("/profiles/")
async def create_profile(profile: Annotated[Profile, Form()], avatar: UploadFile):
    return {"profile": profile, "filename": avatar.filename}