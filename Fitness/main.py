from fastapi import FastAPI

app = FastAPI(title="BFit")

@app.get("/")
def root():
    return {"message": "Hello world"}


@app.get("/pesos/{peso_id}")
def readPeso(peso_id: int):
    return {"peso_id": peso_id}
