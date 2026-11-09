# Frontend
from fastapi import APIRouter, FastAPI
app = FastAPI()

# SIRVE UN FRONTEND
app.frontend("/", directory="dist")


# ROUTING DEL LADO DEL CLIENTE
app.frontend("/", directory="dist", fallback="index.html")


#PAGINA 404 PERSONALIZADA
app.frontend("/", directory="dist", fallback="404.html")


# FALLBACK AUTOMATICO
app.frontend("/", directory="dist")


# DESACTIVA EL FALLBACK
app.frontend("/", directory="dist", fallback=None)


# REVISA EL DIRECTORIO
app.frontend("/", directory="dist", check_dir=False)


# USALO CON APIROUTER
router = APIRouter()
router.frontend("/", directory="dist", fallback="index.html")
app.include_router(router, prefix="/app")