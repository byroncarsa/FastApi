from fastapi import FastAPI
from pydantic import BaseModel
from base_de_datos import base_de_datos

app = FastAPI(title="Mi API de pesos", description="Esta es una API para manejar pesos de usuarios", version="1.0.0")

# MODELOS PYDANTIC
class Usuario(BaseModel):
    id: int
    nombre: str
    fecha_nacimiento: str
    altura: float
    peso_objetivo: float | None = None
    imc: float | None = None
    pesos: list[dict] | None = None
    
class Peso(BaseModel):
    peso_id: int
    peso: float
    fecha: str


# USUARIO
# Traer todos los usuarios
@app.get("/usuarios", tags=["Usuarios"])
def leer_usuarios():
    return base_de_datos


# Mostrar usuario por id
@app.get("/usuarios/{usuario_id}", tags=["Usuarios"])
def leer_usuario(usuario_id: int):
    for user in base_de_datos:
        if user['id'] == usuario_id:
            return user
    return {"message" : "Usuario no encontrado"}


# Agregar usuario
@app.post("/usuarios/", tags=["Usuarios"])
def crear_usuario(usuario: Usuario):
    base_de_datos.append(usuario.model_dump())
    return {"message" : "Usuario creado exitosamente", "usuario" : usuario}


# Editar usuario{
@app.put("/usuarios/{usuario_id}", tags=["Usuarios"])
def editar_usuario(usuario_id: int, usuario: Usuario):
    for user in base_de_datos:
        if user['id'] == usuario_id:
            user.update(usuario.model_dump())
            return {"message" : "Usuario actualizado exitosamente", "usuario" : user}
    return {"message" : "Usuario no encontrado"}
