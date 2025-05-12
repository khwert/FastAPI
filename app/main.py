from fastapi import FastAPI
from .database import lifespan
from .routers import users

app = FastAPI(lifespan=lifespan)
app.include_router(users.router)

# Optional root endpoint
@app.get("/")
def root():
    return {"message": "API is running"}