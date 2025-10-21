from fastapi import FastAPI
from .auth.router import router as auth_router


app = FastAPI(title="test app", version="1.0.0")


app.include_router(auth_router)
