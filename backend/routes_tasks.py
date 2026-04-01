"""
Task API Routes
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Task
from logger import log_request, log_response, log_error, log_database_operation
from datetime import datetime

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# GET all tasks for a user
@router.get("/")
async def get_tasks(
    user_id: str,
    completed: bool = None,
    priority: str = None,
    limit: int = 50,
    offset: int = 0,
    db: Session = Depends(get_db)
):
    """
    Get all tasks for a user with optional filters
    Query params:
    - user_id: User ID (required)
    - completed: Filter by completion status (optional)
    - priority: Filter by priority (optional)
    - limit: How many to return (default: 50)
    - offset: Skip how many (default: 0)
    """
    try:
        log_request("GET", "/api/tasks", user_id=user_id, filters=f"completed={completed}, priority={priority}")
        log_database_operation("SELECT", "tasks", user_id=user_id, completed=completed, priority=priority)
        
        query = db.query(Task).filter(Task.user_id == user_id)
        
        if completed is not None:
            query = query.filter(Task.completed == completed)
        
        if priority:
            query = query.filter(Task.priority == priority)
        
        tasks = query.order_by(Task.created_at.desc()).offset(offset).limit(limit).all()
        
        log_response(200, "/api/tasks", task_count=len(tasks))
        
        return {
            "success": True,
            "data": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "priority": task.priority,
                    "completed": task.completed,
                    "category": task.category,
                    "created_at": task.created_at.isoformat(),
                }
                for task in tasks
            ]
        }
    except Exception as e:
        log_error(f"Failed to fetch tasks for user {user_id}", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# CREATE a new task
@router.post("/")
async def create_task(
    user_id: str,
    title: str,
    description: str = None,
    priority: str = "medium",
    category: str = "work",
    db: Session = Depends(get_db)
):
    """
    Create a new task
    """
    try:
        log_request("POST", "/api/tasks", user_id=user_id, title=title, priority=priority)
        
        new_task = Task(
            user_id=user_id,
            title=title,
            description=description,
            priority=priority,
            category=category,
        )
        
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        
        log_database_operation("INSERT", "tasks", task_id=new_task.id, user_id=user_id)
        log_response(201, "/api/tasks", task_id=new_task.id, action="created")
        
        return {
            "success": True,
            "data": {
                "id": new_task.id,
                "title": new_task.title,
                "priority": new_task.priority,
                "created_at": new_task.created_at.isoformat(),
            }
        }
    except Exception as e:
        db.rollback()
        log_error(f"Failed to create task for user {user_id}", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# UPDATE a task
@router.put("/{task_id}")
async def update_task(
    task_id: str,
    title: str = None,
    description: str = None,
    priority: str = None,
    completed: bool = None,
    category: str = None,
    db: Session = Depends(get_db)
):
    """
    Update an existing task
    """
    try:
        log_request("PUT", f"/api/tasks/{task_id}", task_id=task_id, changes=f"title={title}, priority={priority}, completed={completed}")
        
        task = db.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            log_error(f"Task not found", task_id=task_id)
            raise HTTPException(status_code=404, detail="Task not found")
        
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority is not None:
            task.priority = priority
        if completed is not None:
            task.completed = completed
        if category is not None:
            task.category = category
        
        task.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(task)
        
        log_database_operation("UPDATE", "tasks", task_id=task_id, completed=completed)
        log_response(200, f"/api/tasks/{task_id}", action="updated")
        
        return {
            "success": True,
            "data": {
                "id": task.id,
                "title": task.title,
                "completed": task.completed,
                "priority": task.priority,
                "updated_at": task.updated_at.isoformat(),
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log_error(f"Failed to update task {task_id}", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# DELETE a task
@router.delete("/{task_id}")
async def delete_task(task_id: str, db: Session = Depends(get_db)):
    """
    Delete a task
    """
    try:
        log_request("DELETE", f"/api/tasks/{task_id}", task_id=task_id)
        
        task = db.query(Task).filter(Task.id == task_id).first()
        
        if not task:
            log_error(f"Task not found", task_id=task_id)
            raise HTTPException(status_code=404, detail="Task not found")
        
        db.delete(task)
        db.commit()
        
        log_database_operation("DELETE", "tasks", task_id=task_id)
        log_response(200, f"/api/tasks/{task_id}", action="deleted")
        
        return {"success": True, "message": "Task deleted"}
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        log_error(f"Failed to delete task {task_id}", error=str(e))
        raise HTTPException(status_code=500, detail=str(e))


# GET task statistics
@router.get("/stats/{user_id}")
async def get_stats(user_id: str, db: Session = Depends(get_db)):
    """
    Get task statistics for a user
    """
    try:
        total = db.query(Task).filter(Task.user_id == user_id).count()
        completed = db.query(Task).filter(
            Task.user_id == user_id,
            Task.completed == True
        ).count()
        high_priority = db.query(Task).filter(
            Task.user_id == user_id,
            Task.priority == "high",
            Task.completed == False
        ).count()
        
        return {
            "success": True,
            "data": {
                "total": total,
                "completed": completed,
                "pending": total - completed,
                "high_priority": high_priority,
                "completion_rate": f"{(completed / total * 100):.1f}%" if total > 0 else "0%"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
