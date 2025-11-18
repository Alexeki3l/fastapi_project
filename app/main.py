from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.routers import user_router, auth_router

app = FastAPI(
    title="Proyecto FastAPI Challenge",
    version="1.0.0",
    # root_path="/api",
    docs_url="/",
    description="Descripcion se mostrara aqui."
)

app.include_router(auth_router.router)
app.include_router(user_router.router)

@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    return RedirectResponse(url="/")

@app.get("/api",)
async def root():
    return {"message": "API funcionando correctamente"}
