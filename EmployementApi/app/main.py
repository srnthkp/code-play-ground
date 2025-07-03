"""Main application entry point for FastAPI server."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.routes import auth, items, tasks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # Or ["*"] for all origins (not recommended for production)
    allow_origins=["http://127.0.0.1:3000"],  # client app url
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(auth.router, prefix="/auth")
app.include_router(items.router, prefix="/api")
app.include_router(tasks.router, prefix="/tasks")
