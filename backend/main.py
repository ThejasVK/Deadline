"""
DOIT. Backend API
Python + FastAPI + PostgreSQL + Groq
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
from dotenv import load_dotenv

# Import logging
from logger import log_info, log_error, get_log_file_path, get_log_file_size

# Load environment variables
load_dotenv()

# Import routes
from routes_tasks import router as tasks_router
from routes_ai import router as ai_router
from routes_manager import router as manager_router

# Import database
from database import engine, Base
from models import Task, User, AIResponse

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="DOIT. API",
    description="AI-powered productivity app",
    version="0.1.0"
)

# CORS middleware - allow React frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",      # Local development
        "http://localhost:5173",      # Vite dev server
        "https://doit-app.vercel.app" # Production (Vercel)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(tasks_router)
app.include_router(ai_router)
app.include_router(manager_router)

# Health check endpoint
@app.get("/")
async def root():
    """Health check - API is running"""
    return {
        "status": "✅ DOIT API is running",
        "version": "0.1.0",
        "endpoints": {
            "tasks": "/api/tasks",
            "ai": "/api/ai",
            "logs": "/logs",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    """Detailed health check"""
    try:
        from database import SessionLocal
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_status = "✅ Connected"
    except Exception as e:
        db_status = f"❌ Error: {str(e)}"
    
    try:
        from utils_ai import check_groq_connection
        ai_status = "✅ Connected" if check_groq_connection() else "⚠️  Not connected"
    except:
        ai_status = "⚠️  Not available"
    
    log_info("Health check performed", db=db_status, ai=ai_status)
    
    return {
        "database": db_status,
        "ai": ai_status,
        "environment": os.getenv("ENVIRONMENT", "development")
    }

# Logging endpoints
@app.get("/logs/file")
async def get_logs_file():
    """Download the entire logs file"""
    log_file = get_log_file_path()
    log_info(f"Logs file downloaded: {log_file}")
    return FileResponse(log_file, media_type="text/plain", filename="doit.log")

@app.get("/logs/view")
async def view_logs(lines: int = 100):
    """View last N lines of logs"""
    try:
        log_file = get_log_file_path()
        with open(log_file, 'r') as f:
            all_lines = f.readlines()
        
        last_lines = all_lines[-lines:] if lines > 0 else all_lines
        log_info(f"Logs viewed: {len(last_lines)} lines")
        
        return {
            "total_lines": len(all_lines),
            "displayed_lines": len(last_lines),
            "logs": ''.join(last_lines)
        }
    except Exception as e:
        log_error(f"Error reading logs", error=str(e))
        return {"error": str(e)}

@app.get("/logs/stats")
async def logs_stats():
    """Get logs file statistics"""
    log_file = get_log_file_path()
    size_mb = get_log_file_size()
    
    try:
        with open(log_file, 'r') as f:
            line_count = len(f.readlines())
    except:
        line_count = 0
    
    log_info("Logs statistics retrieved", file_size_mb=size_mb, total_lines=line_count)
    
    return {
        "file": log_file,
        "size_mb": round(size_mb, 2),
        "total_lines": line_count,
        "status": "✅ Logging active"
    }

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    environment = os.getenv("ENVIRONMENT", "development")
    
    print(f"""
    
    🚀 DOIT. Backend Starting...
    
    📍 Server: http://localhost:{port}
    📚 Docs: http://localhost:{port}/docs
    📝 Logs: http://localhost:{port}/logs/stats
    🌍 Environment: {environment}
    
    """)
    
    log_info(f"DOIT Backend started on port {port} | Environment: {environment}")
    
    uvicorn.run(
        "__main__:app",
        host="0.0.0.0",
        port=port,
        reload=(environment == "development")
    )
