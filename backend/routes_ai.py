"""
AI API Routes
"""

from fastapi import APIRouter, HTTPException
from utils_ai import break_down_task, get_motivation, generate_reminder, check_groq_connection
from logger import log_request, log_response, log_error, log_ai_call

router = APIRouter(prefix="/api/ai", tags=["ai"])

# Endpoint to check if Groq is connected
@router.get("/health")
async def ai_health():
    """Check if Groq API is accessible"""
    connected = check_groq_connection()
    return {
        "connected": connected,
        "message": "✅ Groq API is ready!" if connected else "❌ Cannot connect to Groq API"
    }


# Break down a task
@router.post("/break-down")
async def break_down(data: dict):
    """
    Break down a task into subtasks using AI
    Body: { "task_title": "Do laundry" }
    """
    try:
        if "task_title" not in data:
            log_error("Missing task_title in request")
            raise HTTPException(status_code=400, detail="Missing task_title")
        
        task_title = data["task_title"]
        log_request("POST", "/api/ai/break-down", task_title=task_title)
        log_ai_call("break_down_task", task_title)
        
        subtasks = break_down_task(task_title)
        
        log_response(200, "/api/ai/break-down", subtasks_count=len(subtasks))
        
        return {
            "success": True,
            "task": task_title,
            "subtasks": subtasks
        }
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error breaking down task: {task_title}", error=str(e))
        raise HTTPException(status_code=500, detail=f"Error breaking down task: {str(e)}")


# Get motivation
@router.post("/motivation")
async def get_motivation_message(data: dict):
    """
    Get a motivational message for a task
    Body: { "task_title": "Study for exam" }
    """
    try:
        if "task_title" not in data:
            log_error("Missing task_title in request")
            raise HTTPException(status_code=400, detail="Missing task_title")
        
        task_title = data["task_title"]
        log_request("POST", "/api/ai/motivation", task_title=task_title)
        log_ai_call("get_motivation", task_title)
        
        message = get_motivation(task_title)
        
        log_response(200, "/api/ai/motivation", message_length=len(message))
        
        return {
            "success": True,
            "task": task_title,
            "message": message
        }
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error getting motivation for task: {task_title}", error=str(e))
        raise HTTPException(status_code=500, detail=f"Error getting motivation: {str(e)}")


# Get reminder
@router.post("/reminder")
async def get_reminder_message(data: dict):
    """
    Generate a task reminder
    Body: { "task_title": "Submit assignment" }
    """
    try:
        if "task_title" not in data:
            log_error("Missing task_title in request")
            raise HTTPException(status_code=400, detail="Missing task_title")
        
        task_title = data["task_title"]
        log_request("POST", "/api/ai/reminder", task_title=task_title)
        log_ai_call("generate_reminder", task_title)
        
        reminder = generate_reminder(task_title)
        
        log_response(200, "/api/ai/reminder", reminder_length=len(reminder))
        
        return {
            "success": True,
            "task": task_title,
            "reminder": reminder
        }
    except HTTPException:
        raise
    except Exception as e:
        log_error(f"Error generating reminder for task: {task_title}", error=str(e))
        raise HTTPException(status_code=500, detail=f"Error generating reminder: {str(e)}")
