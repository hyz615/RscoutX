from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os

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


# Health check
@app.get(f"{settings.API_V1_PREFIX}/health")
async def health_check():
    return {"status": "healthy"}


# Include routers (API routes must be registered BEFORE static files)
app.include_router(teams.router, prefix=settings.API_V1_PREFIX)
app.include_router(robots.router, prefix=settings.API_V1_PREFIX)
app.include_router(drivers.router, prefix=settings.API_V1_PREFIX)
app.include_router(matches.router, prefix=settings.API_V1_PREFIX)
app.include_router(path.router, prefix=settings.API_V1_PREFIX)
app.include_router(report.router, prefix=settings.API_V1_PREFIX)


# Mount static files (frontend)
frontend_dir = Path(__file__).parent.parent.parent / "frontend"
root_dir = Path(__file__).parent.parent.parent

if frontend_dir.exists() and os.path.isdir(frontend_dir):
    # Mount static files for assets
    app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")
    
    # Serve pushback_map.png from root directory
    @app.get("/pushback_map.png")
    async def serve_map():
        map_file = root_dir / "pushback_map.png"
        if map_file.exists():
            return FileResponse(str(map_file))
        # Fallback to frontend directory
        frontend_map = frontend_dir / "pushback_map.png"
        if frontend_map.exists():
            return FileResponse(str(frontend_map))
        return JSONResponse(
            status_code=404,
            content={"detail": "pushback_map.png not found"}
        )
    
    # Serve index.html at root
    @app.get("/")
    async def serve_frontend():
        index_file = frontend_dir / "index.html"
        if index_file.exists():
            return FileResponse(str(index_file))
        return {"message": "Frontend not found", "docs": f"{settings.API_V1_PREFIX}/docs"}
else:
    # Fallback root endpoint if frontend not found
    @app.get("/")
    async def root():
        return {
            "message": "Welcome to RscoutX API",
            "version": settings.VERSION,
            "docs": f"{settings.API_V1_PREFIX}/docs"
        }
    print(f"Warning: Frontend directory not found at {frontend_dir}")


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
