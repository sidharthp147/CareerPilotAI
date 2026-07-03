import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from services.authentication_service import send_verification_email
from routers import authentication, jobs, recruiters, admin, users, AI,websocket
from slowapi.middleware import SlowAPIMiddleware
from core.limiter import limiter
from slowapi.errors import RateLimitExceeded
from core.exceptions import rate_limit_handler
from core.middleware import block_middleware, logging_middleware
from core.database import Base, engine
from core.logging import setup_logging
from fastapi.responses import JSONResponse
from fastapi import Request    
from prometheus_fastapi_instrumentator import Instrumentator
import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
Base.metadata.create_all(bind=engine)
setup_logging() 
logger=logging.getLogger(__name__)
app = FastAPI()
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

Instrumentator().instrument(app).expose(app)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:8000", "http://localhost:8000", "http://localhost:5173","https://career-pilot-ai-147.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(block_middleware)
app.middleware("http")(logging_middleware)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_handler)
@app.get("/health")
def health_check():
    return {"status": "ok"}
app.include_router(authentication.router)
app.include_router(jobs.router)
app.include_router(recruiters.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(AI.router)
app.include_router(websocket.router)
