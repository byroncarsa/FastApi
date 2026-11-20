
from fastapi import FastAPI, Query, Body, HTTPException, Path
from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Optional, List, Union, Literal
from math import ceil

app = FastAPI(title="Mini Blog")

BLOG_POST = [
    {"id": 1, "title": "Hola desde FastAPI",
        "content": "Mi primer post con FastAPI"},
    {"id": 2, "title": "Mi segundo Post con FastAPI",
        "content": "Mi segundo post con FastAPI blablabla"},
    {"id": 3, "title": "Django vs FastAPI",
        "content": "FastAPI es más rápido por x razones",
        "tags": [
            {"name": "Python"},
            {"name": "fastapi"},
            {"name": "Django"}
        ]},
    {"id": 4, "title": "Hola desde FastAPI",
        "content": "Mi primer post con FastAPI"},
    {"id": 5, "title": "Mi segundo Post con FastAPI",
        "content": "Mi segundo post con FastAPI blablabla"},
    {"id": 6, "title": "Django vs FastAPI",
        "content": "FastAPI es más rápido por x razones"},
    {"id": 7, "title": "Hola desde FastAPI",
        "content": "Mi primer post con FastAPI"},
    {"id": 8, "title": "Mi segundo Post con FastAPI",
        "content": "Mi segundo post con FastAPI blablabla"},
    {"id": 9, "title": "Django vs FastAPI",
        "content": "FastAPI es más rápido por x razones"},
    {"id": 10, "title": "Hola desde FastAPI",
        "content": "Mi primer post con FastAPI"},
    {"id": 11, "title": "Mi segundo Post con FastAPI",
        "content": "Mi segundo post con FastAPI blablabla"},
    {"id": 12, "title": "Django vs FastAPI",
        "content": "FastAPI es más rápido por x razones",
        "tags": [
            {"name": "Python"},
            {"name": "fastapi"},
            {"name": "Django"}
        ]},
    {"id": 13, "title": "Hola desde FastAPI",
        "content": "Mi primer post con FastAPI"},
    {"id": 14, "title": "Mi segundo Post con FastAPI",
        "content": "Mi segundo post con FastAPI blablabla"},
    {"id": 15, "title": "Django vs FastAPI",
        "content": "FastAPI es más rápido por x razones",
        "tags": [
            {"name": "Python"},
            {"name": "fastapi"},
            {"name": "Django"}
        ]},
]


class Tag(BaseModel):
    name: str = Field(..., min_length=2, max_length=30,
                      description="Nombre de la etiqueta")


class Author(BaseModel):
    name: str
    email: EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    tags: Optional[List[Tag]] = Field(default_factory=list)  # []
    author: Optional[Author] = None


class PostCreate(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Titulo del post (mínimo 3 caracteres, máximo 100)",
        examples=["Mi primer post con FastAPI"]
    )
    content: Optional[str] = Field(
        default="Contenido no disponible",
        min_length=10,
        description="Contenido del post (mínimo 10 caracteres)",
        examples=["Este es un contenido válido porque tiene 10 caracteres o más"]
    )
    tags: List[Tag] = Field(default_factory=list)  # []
    author: Optional[Author] = None

    @field_validator("title")
    @classmethod
    def not_allowed_title(cls, value: str) -> str:
        if "spam" in value.lower():
            raise ValueError("El título no puede contener la palabra: 'spam'")
        return value


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    content: Optional[str] = None


class PostPublic(PostBase):
    id: int


class PostSummary(BaseModel):
    id: int
    title: str


class PaginatedPost(BaseModel):
    page: int
    per_page: int
    total: int
    total_pages: int
    has_prev: bool
    has_next: bool
    order_by: Literal["id", "title"]
    direction: Literal["asc", "desc"]
    search: Optional[str] = None
    items: List[PostPublic]


@app.get("/")
def home():
    return {'message': 'Bienvenidos a Mini Blog por Devtalles'}


c


@app.get("/posts/by-tags", response_model=List[PostPublic])
def filter_by_tags(
    tags: List[str] = Query(
        ...,
        min_length=2,
        description="Una o más etiquetas. Ejemplo: ?tags=python&tags=fastapi"
    )
):
    tags_lower = [tag.lower() for tag in tags]

    return [
        post for post in BLOG_POST if any(tag["name"].lower() in tags_lower for tag in post.get("tags", []))
    ]


@app.get("/posts/{post_id}", response_model=Union[PostPublic, PostSummary], response_description="Post encontrado")
def get_post(post_id: int = Path(
    ...,
    ge=1,
    title="ID del post",
    description="Identificador entero del post. Debe ser mayor a 1",
    example=1
), include_content: bool = Query(default=True, description="Incluir o no el contenido")):
    for post in BLOG_POST:
        if post["id"] == post_id:
            if not include_content:
                return {"id": post["id"], "title": post["title"]}
            return post

    return HTTPException(status_code=404, detail="Post no encontrado")


@app.post("/posts", response_model=PostPublic, response_description="Post creado (OK)")
def create_post(post: PostCreate):
    new_id = (BLOG_POST[-1]["id"]+1) if BLOG_POST else 1
    new_post = {"id": new_id,
                "title": post.title,
                "content": post.content,
                "tags": [tag.model_dump() for tag in post.tags],
                "author": post.author.model_dump() if post.author else None
                }
    BLOG_POST.append(new_post)
    return new_post


@app.put("/posts/{post_id}", response_model=PostPublic, response_description="Post actualizado", response_model_exclude_none=True)
def update_post(post_id: int, data: PostUpdate):
    for post in BLOG_POST:
        if post["id"] == post_id:
            # {"title": "Ricardo", "content": None}
            playload = data.model_dump(exclude_unset=True)
            if "title" in playload:
                post["title"] = playload["title"]
            if "content" in playload:
                post["content"] = playload["content"]
            return post

    raise HTTPException(status_code=404, detail="Post no encontrado")


@app.delete("/posts/{post_id}", status_code=204)
def delete_post(post_id: int):
    for index, post in enumerate(BLOG_POST):
        if post["id"] == post_id:
            BLOG_POST.pop(index)
            return
    raise HTTPException(status_code=404, detail="Post no encontrado")


"""
{
  "page": 2,
  "per_page": 3,
  "total": 8,
  "total_pages": 3,
  "has_prev": true,
  "has_next": true,
  "order_by": "title",
  "direction": "asc",
  "search": "fastapi",
  "items": [
    {
      "id": 4,
      "title": "FastAPI avanzado",
      "content": "Ejemplo de post avanzado"
    },
    {
      "id": 5,
      "title": "FastAPI básico",
      "content": "Ejemplo de post básico"
    },
    {
      "id": 6,
      "title": "FastAPI con seguridad",
      "content": "Post sobre seguridad con FastAPI"
    }
  ]
}
"""