from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Mi API de pesos", description="Esta es una API para manejar pesos de usuarios", version="1.0.0")
    
    
# BASE DE DATOS SIMULADA
base_de_datos = [
    {
        "id" : 1,
        "nombre" : "Byron",
        "fecha_nacimiento" : "1994-08-13",
        "altura" : 1.72,
        "peso_objetivo" : 80,
        "imc" : 60,
        "pesos" : [
            {
                "peso_id" : 1,
                "peso" : 99.9,
                "fecha" : "2025-12-26"
            },
            {
                "peso_id" : 2,
                "peso" : 75,
                "fecha" : "2025-12-26"
            }
        ]
    },
    {
        "id" : 2,
        "nombre" : "Juan",
        "fecha_nacimiento" : "1995-05-15",
        "altura" : 1.78,
        "peso_objetivo" : 70,
        "imc" : 50,
        "pesos" : [
            {
                "peso_id" : 1,
                "peso" : 80.9,
                "fecha" : "2025-12-26"
            },
            {
                "peso_id" : 2,
                "peso" : 79.8,
                "fecha" : "2025-12-26"
            }
        ]
    }
]


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


#INICIO
@app.get("/")
async def root():
    return {"message": "Hola mundo, esta es mi API de pesos"}


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



# # PESOS
# # Trae pesos por usuario 
# @app.get("/usuarios/{usuario_id}/pesos", tags=["Pesos"])
# def leer_pesos_usuario(usuario_id : int, incluir_usuario : bool = False, skip: int = 0, limit: int = 10):
#     for user in base_de_datos:
#         if user['id'] == usuario_id:
#             if incluir_usuario:
#                 return {"usuario" : user['nombre'], "pesos" : user['pesos'][skip : skip + limit]}
#             return user['pesos'][skip : skip + limit]
#     return {"message" : "Usuario no encontrado"}


# # Traer el ultimo peso
# @app.get("/usuario/{usuario_id}/pesos/ultimo", tags=["Pesos"])
# def leer_ultimo_peso_usuario(usuario_id : int):
#     for user in base_de_datos:
#         if user['id'] == usuario_id:
#             if user['pesos']:
#                 return user['pesos'][-1]
#             return {"message" : "No hay pesos registrados para este usuario"}
#         return {"message" : "Usuario no encontrado"}
    
    
# # Agregar un peso
# @app.post("/usuarios/{usuario_id}/pesos", tags=["Pesos"])
# def agregar_peso(usuario_id: int, peso: Peso):
#     for user in base_de_datos:
#         if user['id'] == usuario_id:
#             user['pesos'].append(peso.model_dump())
#             return{"message" : "Peso agregado existosamente", "peso" : peso}
#         return {"message" : "Usuario no encontrado"}
    
    
# # Editar un peso
# @app.put("/usuarios/{usuario_id}/pesos/{peso_id}", tags=["Pesos"])
# def editar_peso(usuario_id: int, peso_id: int, peso: Peso):
#     for user in base_de_datos:
#         if user['id'] == usuario_id:
#             for peso in user['pesos']:
#                 if peso['peso_id'] == peso_id:
#                     peso.update(peso.model_dump())
#                     return {"message" : "Peso actualizado existosamente", "peso" : peso}
#                 return {"message" : "Peso no encontrado"}
#         return {"message" : "Usuario no encontrado"}
    

# # PESO OBJETIVO
# # Agregar peso objetivo
# @app.post("/usuarios/{usuario_id}/peso_objetivo", tags=["Peso Objetivo"])
# def agregar_peso_objetivo(usuario_id: int, peso_objetivo: float):
#     for user in base_de_datos:
#         if user['id'] == usuario_id:
#             user['peso_objetivo'] = peso_objetivo
#             return {"message" : "Peso objetivo agregado existosamente", "peso_objetivo" : peso_objetivo}
#         return {"message" : "Usuario no encontrado"}
    
# # Editar peso objetivo
# # Eliminar peso objetivo


# # DEFINIR
# # Peso ideal
# # Definir IMC
    

