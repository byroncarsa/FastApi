# Validaciones cuerpo ymodelos anidados
from fastapi import FastAPI, Path, Query, Body
from typing import Annotated
from pydantic import BaseModel, Field
from base_de_datos import base_de_datos

app = FastAPI(title="Mi API de pesos", description="Esta es una API para manejar pesos de usuarios", version="1.0.0")

# MODELOS PYDANTIC
class Peso(BaseModel):
    id: int
    peso: float
    fecha : str

class Usuario(BaseModel):
    id: int
    nombre: str = Field(title="Nombre del usuario", min_length=5, max_length=50)
    fecha_nacimiento: str
    altura: float = Field(gt=0, description="La altura debe ser mayor a 0") 
    peso_objetivo: float = Field(default=None, gt=0, description="El peso debe ser mayor a 0") 
    imc: float = Field(default=None, gt=0, description="El imc debe ser mayor a 0") 
    pesos: list[Peso] | None = None
    
    
# USUARIO
# Traer todos los usuarios
@app.get("/usuarios", tags=["Usuarios"])
def leer_usuarios(
    skip: Annotated[int, Query(title="Definir inicio")] = 0, 
    limit: Annotated[int, Query(title="Definir limite")] = 10
):
    return base_de_datos[skip : skip + limit]


# Mostrar usuario por id
@app.get("/usuarios/{usuario_id}", tags=["Usuarios"])
def leer_usuario(
    usuario_id: Annotated[int, Path(title="El id del usuario a obtener", ge= 1, le=1000)], 
    incluir_pesos: bool = False
):
    for user in base_de_datos:
        if user['id'] == usuario_id:
            if not incluir_pesos:
                usuario = user.copy()
                usuario.pop('pesos', None)
                return usuario
            return user
    return {"message" : "Usuario no encontrado"}


# Agregar usuario
@app.post("/usuarios/", tags=["Usuarios"])
def crear_usuario(usuario: Annotated[Usuario, Body(embed=True)]):
    base_de_datos.append(usuario.model_dump())
    return {"message" : "Usuario creado exitosamente", "usuario" : usuario}


# Editar usuario{
@app.put("/usuarios/{usuario_id}", tags=["Usuarios"])
def editar_usuario(
    usuario_id: Annotated[int, Path(title="El id del usuario a editar", ge= 1, le=1000)], 
    usuario: Annotated[Usuario, Body(embed=True)]
):
    for user in base_de_datos:
        if user['id'] == usuario_id:
            user.update(usuario.model_dump())
            return {"message" : "Usuario actualizado exitosamente", "usuario" : user}
    return {"message" : "Usuario no encontrado"}
