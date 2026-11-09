# Archivos Estáticos
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()


# USA STATICFILES
app.mount("/static", StaticFiles(directory="static"), name="static")