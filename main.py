
from fastapi import FastAPI, Query, Body, HTTPException

app = FastAPI(title="Fitness")

BLOG_POST = [
    {"id": 1, "title": "Hola desde FastAPI", "Content":"Mi primer post con FastAPI"},
    {"id": 2, "title": "Mi segundo Post con FastAPI", "Content":"Mi segundo post con FastAPI blablabla"},
    {"id": 3, "title": "Django vs FastAPI", "Content":"FastAPI es más rápido por x razones"},
]

PESOS = [
    {"id": 1, "peso": 79, "fecha":"Lunes"},
    {"id": 2, "peso": 78, "fecha":"Martes"},
    {"id": 3, "peso": 77, "fecha":"Miercoles"},
]


@app.get("/")
def home():
    return {'message': 'Bienvenidos a Fitness App por Byron'}


@app.get("/pesos")
def list_pesos(query: str | None = Query(default=None, description="Texto para buscar por dia")):
    if query:
        results = [peso for peso in PESOS if query.lower() in peso["fecha"].lower()]
        return {"data": results, "query": query}
    return {"data": PESOS}


@app.get("/posts")
def list_posts(query: str | None = Query(default=None, description="Texto para buscar por título")):
    if query:
        results = [post for post in BLOG_POST if query.lower() in  post["title"].lower() ]
        return {"data": results, "query": query}
    return {"data": BLOG_POST}
 

@app.get("/posts", response_model=List[PostPublic])
def list_posts(query: str | None = Query(default=None, description="Texto para buscar por título")):
    
    if query:
        return [post for post in BLOG_POST if query.lower() in  post["title"].lower() ]
    
    return BLOG_POST
 