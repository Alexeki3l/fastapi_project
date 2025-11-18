from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from app.routers import post_router, tag_router, user_router, auth_router

app = FastAPI(
    title="Proyecto FastAPI Challenge",
    version="1.0.0",
    docs_url="/",
    description="Descripcion se mostrara aqui."
)

app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(post_router.router)
app.include_router(tag_router.router)
