from fastapi import FastAPI

from .auth.router import router as auth_router
from .users.router import router as user_router


app = FastAPI(title="test app", version="1.0.0")


app.include_router(auth_router)
app.include_router(user_router)
