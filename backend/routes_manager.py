"""
Manager API Routes - Progress tracking and deadline management
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Task
from utils_manager import (
    get_deadline_warning,
    request_progress_update,
    generate_progress_report,
    get_manager_feedback,
    get_weekly_standup
)
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/manager", tags=["manager"])


# Get all tasks with status for manager view
@router.get("/tasks/{user_id}")
async def get_manager_view(user_id: str, db: Session = Depends(get_db)):
    """
    Get all tasks with their status and deadlines
    """
    try:
        tasks = db.query(Task).filter(Task.user_id == user_id).order_by(Task.due_date).all()
        
        # Categorize tasks
        overdue = []
        due_soon = []
        in_progress = []
        blocked = []
        completed_tasks = []
        
        now = datetime.utcnow()
        
        for task in tasks:
            task_data = {
                "id": task.id,
                "title": task.title,
                "status": task.status,
                "priority": task.priority,
                "progress": task.progress_percentage,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "category": task.category,
            }
            
            if task.status == "completed":
                completed_tasks.append(task_data)
            elif task.status == "blocked":
                blocked.append(task_data)
            elif task.status == "in_progress":
                in_progress.append(task_data)
            elif task.due_date and task.due_date < now:
                overdue.append(task_data)
            elif task.due_date and (task.due_date - now).days <= 3:
                due_soon.append(task_data)
        
        return {
            "success": True,
            "data": {
                "overdue": overdue,
                "due_soon": due_soon,
                "in_progress": in_progress,
                "blocked": blocked,
                "completed": completed_tasks,
                "stats": {
                    "total": len(tasks),
                    "completed": len(completed_tasks),
                    "in_progress": len(in_progress),
                    "blocked": len(blocked),
                    "overdue": len(overdue),
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get deadline warnings
@router.get("/warnings/{user_id}")
async def get_deadline_warnings(user_id: str, db: Session = Depends(get_db)):
    """
    Get all deadline warnings and urgent updates needed
    """
    try:
        tasks = db.query(Task).filter(
            Task.user_id == user_id,
            Task.status != "completed"
        ).all()
        
        warnings = []
        now = datetime.utcnow()
        
        for task in tasks:
            if not task.due_date:
                continue
            
            days_remaining = (task.due_date - now).days
            
            # Only show urgent warnings
            if days_remaining <= 3:  # Due within 3 days or overdue
                warning = get_deadline_warning(task.title, task.due_date.isoformat(), days_remaining)
                warnings.append({
                    "task_id": task.id,
                    "task_title": task.title,
                    "days_remaining": days_remaining,
                    "warning": warning,
                    "is_overdue": days_remaining < 0
                })
        
        return {
            "success": True,
            "urgent_warnings": len([w for w in warnings if w['days_remaining'] <= 0]),
            "warnings": warnings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Request progress update
@router.post("/request-update")
async def request_update(user_id: str, task_id: str, db: Session = Depends(get_db)):
    """
    Manager requests a status update
    """
    try:
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        days_since_update = 0
        if task.last_status_update:
            days_since_update = (datetime.utcnow() - task.last_status_update).days
        
        update_request = request_progress_update(task.title, task.status, days_since_update)
        
        # Increment reminder count
        task.manager_reminder_count = str(int(task.manager_reminder_count) + 1)
        db.commit()
        
        return {
            "success": True,
            "task_id": task.id,
            "message": update_request,
            "reminder_count": int(task.manager_reminder_count)
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Generate progress report
@router.get("/progress-report/{user_id}")
async def get_progress_report(user_id: str, db: Session = Depends(get_db)):
    """
    Generate a progress report for all user tasks
    """
    try:
        tasks = db.query(Task).filter(Task.user_id == user_id).all()
        
        tasks_data = [
            {
                "title": t.title,
                "status": t.status,
                "progress": int(t.progress_percentage)
            }
            for t in tasks
        ]
        
        report = generate_progress_report(tasks_data)
        
        # Calculate stats
        total = len(tasks)
        completed = len([t for t in tasks if t.status == "completed"])
        in_progress = len([t for t in tasks if t.status == "in_progress"])
        blocked = len([t for t in tasks if t.status == "blocked"])
        
        return {
            "success": True,
            "report": report,
            "stats": {
                "total_tasks": total,
                "completed": completed,
                "in_progress": in_progress,
                "blocked": blocked,
                "completion_rate": f"{(completed/total*100):.1f}%" if total > 0 else "0%"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Get manager feedback for a task
@router.post("/feedback")
async def get_feedback(user_id: str, task_id: str, db: Session = Depends(get_db)):
    """
    Get manager feedback on a specific task
    """
    try:
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        feedback = get_manager_feedback(task.title, task.status, task.progress_percentage)
        
        return {
            "success": True,
            "task_id": task.id,
            "feedback": feedback,
            "current_status": task.status,
            "current_progress": task.progress_percentage
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Weekly standup
@router.get("/weekly-standup/{user_id}")
async def get_standup(user_id: str, db: Session = Depends(get_db)):
    """
    Manager's weekly standup message
    """
    try:
        tasks = db.query(Task).filter(Task.user_id == user_id).all()
        
        tasks_data = [
            {"title": t.title, "status": t.status}
            for t in tasks
        ]
        
        standup = get_weekly_standup(tasks_data)
        
        return {
            "success": True,
            "standup": standup,
            "generated_at": datetime.utcnow().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Update task status and progress
@router.put("/task-update/{task_id}")
async def update_task_status(
    task_id: str,
    user_id: str,
    status: str = None,
    progress: str = None,
    db: Session = Depends(get_db)
):
    """
    Update task status and progress
    Statuses: not_started, in_progress, blocked, completed
    """
    try:
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        if status:
            task.status = status
        
        if progress:
            task.progress_percentage = str(min(100, max(0, int(progress))))
        
        task.last_status_update = datetime.utcnow()
        db.commit()
        db.refresh(task)
        
        # Get manager feedback on the update
        feedback = get_manager_feedback(task.title, task.status, task.progress_percentage)
        
        return {
            "success": True,
            "task_updated": {
                "id": task.id,
                "status": task.status,
                "progress": task.progress_percentage,
            },
            "manager_feedback": feedback
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
