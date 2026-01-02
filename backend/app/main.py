from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.db.session import init_db
from app.api.routes import teams, robots, drivers, matches, path, report

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    redoc_url=f"{settings.API_V1_PREFIX}/redoc",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to RscoutX API",
        "version": settings.VERSION,
        "docs": f"{settings.API_V1_PREFIX}/docs"
    }


# Health check
@app.get(f"{settings.API_V1_PREFIX}/health")
async def health_check():
    return {"status": "healthy"}


# Include routers
app.include_router(teams.router, prefix=settings.API_V1_PREFIX)
app.include_router(robots.router, prefix=settings.API_V1_PREFIX)
app.include_router(drivers.router, prefix=settings.API_V1_PREFIX)
app.include_router(matches.router, prefix=settings.API_V1_PREFIX)
app.include_router(path.router, prefix=settings.API_V1_PREFIX)
app.include_router(report.router, prefix=settings.API_V1_PREFIX)


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print("Database initialized")


# Exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
