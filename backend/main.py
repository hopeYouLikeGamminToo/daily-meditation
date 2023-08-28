from api.user import router as user_router
from api.content import router as content_router

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.include_router(user_router, tags=["User"])
app.include_router(content_router, tags=["Content"])


origins = [
    "http://localhost:8888",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root() -> dict:
    return {"FastAPI": "Navigate to /docs to see the API documentation."}

# see /backend/api/ for other endpoints