from fastapi import FastAPI
from auth import router as auth_route
from api import router as api_router
app = FastAPI()

app.include_router(auth_route)
app.include_router(api_router)


