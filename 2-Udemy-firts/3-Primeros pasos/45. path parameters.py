from fastapi import FastAPI, Query

app = FastAPI(title="Mini Blog")

BLOG_POST = [
    {"id":1, "title":"primer articulo", "content":"contenido articulo 1"},
    {"id":2, "title":"segundo articulo", "content":"contenido articulo 2"},
    {"id":3, "title":"tercer articulo", "content":"contenido articulo 3"}
]

@app.get('/')
def home():
    return {'message':'bienvenido a mi blog'}


@app.get("/posts")
def list_posts(query: str | None = Query(default=None, description="Texto para buscar por titulo") ):
    if query:
        results = [post for post in BLOG_POST if query.lower() in post['title'].lower()]
        return {'data':results, 'query': query}
    return {"data":BLOG_POST}


@app.get("/posts/{post_id}")
def get_post(post_id: int):
    for post in BLOG_POST:
        if post['id'] == post_id:
            return {'data': post}
    return {'data': 'Post no encontrado'}    

    