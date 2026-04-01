"""
DOIT. Backend API - Simplified version (no database required)
Python + FastAPI + Groq
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="DOIT. API",
    description="AI-powered productivity app",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",
        "https://doit-app.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple in-memory task storage (for testing)
tasks_db = {}
next_task_id = 1

# Health check
@app.get("/")
async def root():
    """Health check"""
    return {
        "status": "✅ DOIT API is running",
        "version": "0.1.0",
        "mode": "development",
        "endpoints": [
            "/api/tasks",
            "/api/ai/break-down",
            "/api/ai/motivation",
            "/docs"
        ]
    }

@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "running",
        "database": "in-memory (testing mode)",
        "ai": "ready if GROQ_API_KEY set"
    }

# Tasks Endpoints
@app.get("/api/tasks/")
async def get_tasks(user_id: str = "test-user"):
    """Get all tasks for a user"""
    user_tasks = [t for t in tasks_db.values() if t.get("user_id") == user_id]
    return {
        "success": True,
        "data": user_tasks
    }

@app.post("/api/tasks/")
async def create_task(
    user_id: str = "test-user",
    title: str = None,
    description: str = None,
    priority: str = "medium",
    category: str = "work"
):
    """Create a new task"""
    global next_task_id
    
    if not title:
        return {"success": False, "error": "title required"}
    
    task_id = str(next_task_id)
    next_task_id += 1
    
    task = {
        "id": task_id,
        "user_id": user_id,
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "completed": False,
        "created_at": "2026-04-01T00:00:00"
    }
    
    tasks_db[task_id] = task
    
    return {
        "success": True,
        "data": task
    }

@app.put("/api/tasks/{task_id}")
async def update_task(
    task_id: str,
    title: str = None,
    completed: bool = None,
    priority: str = None
):
    """Update a task"""
    if task_id not in tasks_db:
        return {"success": False, "error": "Task not found"}
    
    task = tasks_db[task_id]
    if title:
        task["title"] = title
    if completed is not None:
        task["completed"] = completed
    if priority:
        task["priority"] = priority
    
    return {
        "success": True,
        "data": task
    }

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a task"""
    if task_id in tasks_db:
        del tasks_db[task_id]
        return {"success": True, "message": "Task deleted"}
    return {"success": False, "error": "Task not found"}

# AI Endpoints
@app.post("/api/ai/break-down")
async def break_down(data: dict):
    """Break down a task into subtasks"""
    from utils_ai import break_down_task
    
    task_title = data.get("task_title", "Do something")
    subtasks = break_down_task(task_title)
    
    return {
        "success": True,
        "task": task_title,
        "subtasks": subtasks
    }

@app.post("/api/ai/motivation")
async def motivation(data: dict):
    """Get motivation for a task"""
    from utils_ai import get_motivation
    
    task_title = data.get("task_title", "tasks")
    message = get_motivation(task_title)
    
    return {
        "success": True,
        "task": task_title,
        "message": message
    }

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 DOIT Backend Starting (Simplified Mode)\n")
    print("📍 Server: http://localhost:8000")
    print("📚 Docs: http://localhost:8000/docs\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
