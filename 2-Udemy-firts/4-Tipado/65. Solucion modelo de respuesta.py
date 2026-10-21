from fastapi import FastAPI, Query, Body, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Union

app = FastAPI(title="Mini Blog")

BLOG_POST = [
    {"id":1, "title":"primer articulo", "content":"contenido articulo 1"},
    {"id":2, "title":"segundo articulo", "content":"contenido articulo 2"},
    {"id":3, "title":"tercer articulo", "content":"contenido articulo 3"}
]


class PostBase(BaseModel):
    title: str
    content: Optional[str] = "Contenido por defecto"
    
class PostCreate(BaseModel):
    title: str = Field(
        ...,
        min_length= 3,
        max_length= 100,
        description= "Titulo del post (minimo 3 caracteres y maximo 100 caracteres)",
        examples= ['Mi primer post con fastapi']
    )
    title: str = Field(
        default= "Contenido no disponible",
        min_length= 10,
        description= "Contenido del post (minimo 10 caracteres)",
        examples= ['Este es un contenido valido por que tiene 10 caracteres o mas']
    )

class PostUpdate(BaseModel):
    title: str
    content: str
    
# Moldes para respuestas
class PostPublic(PostBase):
    id: int
    
class PostSummary(BaseModel):
    id: int
    title: str


@app.get('/')
def home():
    return {'message':'bienvenido a mi blog'}


@app.get("/posts", response_model=List[PostPublic])
def list_posts(query: str | None = Query(default=None, description="Texto para buscar por titulo") ):
    if query:
        return [post for post in BLOG_POST if query.lower() in post['title'].lower()]
    return BLOG_POST


@app.get("/posts/{post_id}", response_model=Union[PostPublic, PostSummary], response_description="Post encontrado")
def get_post(post_id: int, include_content: bool = Query(default=True, description='Incluir o no el contenido')):
    for post in BLOG_POST:
        if post['id'] == post_id:
            if not include_content:
                return {'id': post['id'], 'title': post['title']}
            return post
    return HTTPException(status_code=404, detail="Post no encontrado")


# @app.post("/posts")
# def create_post(post: dict = Body(...)):
#     if "title" not in post or "content" not in post:
#         return {"error": "Title y Content son requeridos"}
    
#     if not str(post["title"]).strip():
#         return {"error": "Title no puede estar vacío"}
    
#     new_id = (BLOG_POST[-1]["id"]+1) if BLOG_POST else 1
#     new_post = {"id": new_id, "title": post["title"], "content": post["content"]}
#     BLOG_POST.append(new_post)
#     return {"message": "Post creado", "data": new_post}


@app.post('/posts', response_model=PostPublic, response_description="Post creado (OK)")
def create_post(post:PostCreate):
    # Simular id para nuevo post
    new_id = (BLOG_POST[-1]['id']+1) if BLOG_POST else 1
    new_post = {'id': new_id, 'title': post.title, 'content': post.content}
    BLOG_POST.append(new_post)
    return new_post
        
        
# @app.put("/posts/{post_id}")
# def update_post(post_id: int, data: dict = Body(...)):
#     for post in BLOG_POST:
#         if post["id"] == post_id:
#             if "title" in data: post["title"] = data["title"]
#             if "content" in data: post["content"] = data["content"]
#             return {"message": "Post actualizado", "data": post}
    
#     raise HTTPException(status_code=404, detail="Post no encontrado")


@app.put("/posts/{post_id}", response_model=PostPublic, response_description="Post actualizado", response_model_exclude_none=True)
def update_post(post_id: int, data: PostUpdate):
    for post in BLOG_POST:
        if post["id"] == post_id:
            playload = data.model_dump(exclude_unset=True) 
            if "content" in playload: post['content'] = playload['content']
            return post
    raise HTTPException(status_code=404, detail="Post no encontrado")


@app.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int):
    for index, post in enumerate(BLOG_POST):
        if post['id'] == post_id:
            BLOG_POST.pop(index)
            return
    raise HTTPException(status_code=404, detail="Post no encontrado")
