from fastapi import FastAPI

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
def list_posts():
    return {"data":BLOG_POST}