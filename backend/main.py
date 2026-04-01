"""
DOIT Backend - Complete Working Version
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import uuid
import json
from pathlib import Path
import random

# In-memory storage
tasks_db = {}
logs_file = Path("logs") / f"doit-{datetime.now().strftime('%Y-%m-%d')}.log"
logs_file.parent.mkdir(exist_ok=True)

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
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:5173",
        "https://doit-app.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def log_action(level: str, action: str, details: dict = None):
    """Log actions to file and print"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"{timestamp} | {level:8} | {action}"
    if details:
        log_message += f" | {json.dumps(details)}"
    
    print(log_message)
    with open(logs_file, "a") as f:
        f.write(log_message + "\n")

# ==================== HEALTH CHECK ====================
@app.get("/")
async def root():
    log_action("INFO", "GET /")
    return {
        "status": "✅ DOIT API is running",
        "version": "0.1.0",
        "endpoints": {
            "tasks": "/api/tasks/",
            "ai": "/api/ai/",
            "manager": "/api/manager/",
            "logs": "/logs/",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health():
    log_action("INFO", "GET /health")
    return {"status": "ok", "storage": "in-memory"}

# ==================== TASKS API ====================
@app.get("/api/tasks/")
async def get_tasks(user_id: str = "default-user", completed: bool = None, limit: int = 50):
    log_action("INFO", "GET /api/tasks/", {"user_id": user_id})
    
    user_tasks = [t for t in tasks_db.values() if t["user_id"] == user_id]
    
    if completed is not None:
        user_tasks = [t for t in user_tasks if t["completed"] == completed]
    
    user_tasks = sorted(user_tasks, key=lambda x: x["created_at"], reverse=True)[:limit]
    
    return {"success": True, "data": user_tasks, "count": len(user_tasks)}

@app.post("/api/tasks/")
async def create_task(
    user_id: str = "default-user",
    title: str = None,
    description: str = None,
    priority: str = "medium",
    category: str = "work",
    deadline: str = None,
    status: str = "not-started"
):
    if not title:
        raise HTTPException(status_code=400, detail="Missing title")
    
    task_id = str(uuid.uuid4())
    now = datetime.now().isoformat()
    
    new_task = {
        "id": task_id,
        "user_id": user_id,
        "title": title,
        "description": description,
        "priority": priority,
        "category": category,
        "completed": False,
        "status": status,
        "deadline": deadline,
        "created_at": now,
        "updated_at": now
    }
    
    tasks_db[task_id] = new_task
    log_action("INFO", "POST /api/tasks/", {"task_id": task_id, "title": title})
    
    return {"success": True, "data": new_task}

@app.put("/api/tasks/{task_id}")
async def update_task(
    task_id: str,
    title: str = None,
    description: str = None,
    priority: str = None,
    completed: str = None,
    status: str = None,
    deadline: str = None,
    category: str = None,
    progress: str = None
):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks_db[task_id]
    
    if title is not None:
        task["title"] = title
    if description is not None:
        task["description"] = description
    if priority is not None:
        task["priority"] = priority
    if completed is not None:
        # Convert string "true"/"false" to boolean
        task["completed"] = completed.lower() in ("true", "1", "yes")
    if status is not None:
        task["status"] = status
    if deadline is not None:
        task["deadline"] = deadline
    if category is not None:
        task["category"] = category
    if progress is not None:
        try:
            task["progress"] = int(progress)
        except:
            pass
    
    task["updated_at"] = datetime.now().isoformat()
    
    log_action("INFO", "PUT /api/tasks/", {"task_id": task_id, "completed": task.get("completed"), "title": task.get("title")})
    
    # Return simplified response for testing
    return {
        "success": True,
        "data": {
            "id": task.get("id"),
            "title": task.get("title"),
            "completed": task.get("completed"),
            "priority": task.get("priority"),
            "status": task.get("status"),
            "category": task.get("category"),
            "updated_at": task.get("updated_at")
        }
    }

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str):
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    del tasks_db[task_id]
    log_action("INFO", "DELETE /api/tasks/", {"task_id": task_id})
    
    return {"success": True, "message": "Task deleted"}

# ==================== AI API ====================
@app.post("/api/ai/break-down")
async def break_down(task_title: str = None):
    if not task_title:
        raise HTTPException(status_code=400, detail="Missing task_title")
    
    log_action("INFO", "POST /api/ai/break-down", {"task": task_title})
    
    subtasks = [
        f"Plan your approach for: {task_title}",
        f"Start the first step of: {task_title}",
        f"Review progress on: {task_title}",
        f"Complete and verify: {task_title}"
    ]
    
    return {"success": True, "task": task_title, "subtasks": subtasks}

@app.post("/api/ai/motivation")
async def get_motivation(task_title: str = None):
    if not task_title:
        raise HTTPException(status_code=400, detail="Missing task_title")
    
    log_action("INFO", "POST /api/ai/motivation", {"task": task_title})
    
    motivations = [
        f"You can do this! Just take the first step on: {task_title} 💪",
        f"Stop overthinking and start {task_title}! You've got this! 🚀",
        f"This is easier than you think. Let's do {task_title}! ⚡",
        f"Your future self will thank you for finishing {task_title} 🎯"
    ]
    
    message = random.choice(motivations)
    return {"success": True, "task": task_title, "message": message}

@app.post("/api/ai/reminder")
async def get_reminder(task_title: str = None):
    if not task_title:
        raise HTTPException(status_code=400, detail="Missing task_title")
    
    log_action("INFO", "POST /api/ai/reminder", {"task": task_title})
    
    reminders = [
        f"Hey! Remember that {task_title}? It's calling for you! 📞",
        f"Your {task_title} isn't going to complete itself. Let's go! 🔥",
        f"Psst... {task_title} is still waiting for you. Don't delay! ⏰",
        f"Come on, let's finish {task_title} today! 💯"
    ]
    
    reminder = random.choice(reminders)
    return {"success": True, "task": task_title, "reminder": reminder}

# ==================== LOGS API ====================
@app.get("/logs/view")
async def view_logs(lines: int = 50):
    try:
        if logs_file.exists():
            with open(logs_file, "r") as f:
                all_lines = f.readlines()
            recent_lines = all_lines[-lines:]
            return {"success": True, "lines": len(recent_lines), "data": recent_lines}
        return {"success": True, "lines": 0, "data": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/logs/stats")
async def log_stats():
    try:
        if logs_file.exists():
            size = logs_file.stat().st_size
            with open(logs_file, "r") as f:
                lines = len(f.readlines())
            return {
                "success": True,
                "file": str(logs_file),
                "size_bytes": size,
                "size_kb": round(size / 1024, 2),
                "lines": lines
            }
        return {"success": True, "file": str(logs_file), "size_bytes": 0, "lines": 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== MANAGER API ====================
@app.get("/api/manager/stats")
async def get_stats(user_id: str = "default-user"):
    log_action("INFO", "GET /api/manager/stats", {"user_id": user_id})
    
    user_tasks = [t for t in tasks_db.values() if t["user_id"] == user_id]
    
    total = len(user_tasks)
    completed = len([t for t in user_tasks if t["completed"]])
    pending = total - completed
    high_priority = len([t for t in user_tasks if t["priority"] == "high" and not t["completed"]])
    
    stats = {
        "total": total,
        "completed": completed,
        "pending": pending,
        "high_priority": high_priority,
        "completion_rate": f"{(completed / total * 100):.1f}%" if total > 0 else "0%"
    }
    
    return {"success": True, "data": stats}

@app.post("/api/manager/progress-report")
async def progress_report(user_id: str = "default-user"):
    log_action("INFO", "POST /api/manager/progress-report", {"user_id": user_id})
    
    user_tasks = [t for t in tasks_db.values() if t["user_id"] == user_id]
    
    total = len(user_tasks)
    completed = len([t for t in user_tasks if t["completed"]])
    
    report = {
        "week": datetime.now().strftime("%Y-W%W"),
        "total_tasks": total,
        "completed": completed,
        "pending": total - completed,
        "completion_percentage": f"{(completed / total * 100):.1f}%" if total > 0 else "0%",
        "message": f"Great work! You've completed {completed} out of {total} tasks! Keep it up! 🚀"
    }
    
    return {"success": True, "data": report}

if __name__ == "__main__":
    import uvicorn
    log_action("INFO", "STARTUP", {"message": "DOIT Backend Starting..."})
    uvicorn.run(app, host="0.0.0.0", port=8000)
