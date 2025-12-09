"""
Main FastAPI application
Serves both API and static frontend files
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Create FastAPI app
app = FastAPI(
    title="Database Manager API",
    description="Universal database management tool API",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
from api import connections, databases, tables, queries

# Include API routers
app.include_router(connections.router, prefix="/api/connections", tags=["Connections"])
app.include_router(databases.router, prefix="/api/databases", tags=["Databases"])
app.include_router(tables.router, prefix="/api/tables", tags=["Tables"])
app.include_router(queries.router, prefix="/api/queries", tags=["Queries"])

# Serve frontend static files
frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")

if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    async def read_root():
        """Serve frontend index.html"""
        index_path = os.path.join(frontend_path, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"message": "Frontend not found. API is running at /docs"}

else:

    @app.get("/")
    async def read_root():
        return {"message": "Database Manager API is running. Docs at /docs"}


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}


# Cleanup on shutdown
@app.on_event("shutdown")
async def shutdown_event():
    from services.connection_manager import connection_manager

    connection_manager.close_all()
    logging.info("All connections closed")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
