"""
Main FastAPI application entry point.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.database import engine, Base
import app.models  # Ensure all models are registered with Base.metadata
from app.routes import auth, exams, students, departments

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Auto-create tables on startup (useful for dev / docker-compose)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Exam Hall Allocation API",
    version="1.0.0",
    description="Backend API for Smart Exam Hall Allocation and Seating Matrix Management",
    lifespan=lifespan,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local dev / k8s
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api")
app.include_router(exams.router, prefix="/api")
app.include_router(students.router, prefix="/api")
app.include_router(departments.router, prefix="/api")


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "hall-allocation-backend"}


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to Exam Hall Allocation API",
        "docs": "/docs",
        "health": "/health",
    }
