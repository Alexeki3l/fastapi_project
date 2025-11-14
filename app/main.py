from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI(
    title="Proyecto FastAPI Challenge",
    version="1.0.0",
    # root_path="/api",
    docs_url="/",
    description="Descripcion se mostrara aqui."
)

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    return RedirectResponse(url="/")

@app.get("/api",)
async def root():
    return {"message": "API funcionando correctamente"}
