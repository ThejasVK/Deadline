"""
AI Integration with Groq API
"""

import os
from groq import Groq

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("⚠️  Warning: GROQ_API_KEY not set in .env")

client = Groq(api_key=GROQ_API_KEY)

def break_down_task(task_title: str) -> list:
    """
    Break down a task into subtasks using Groq API
    Returns: ["subtask 1", "subtask 2", ...]
    """
    try:
        message = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""Break down this task into 3-5 small, actionable subtasks.

Task: {task_title}

Format your response as a numbered list with ONLY the subtasks, nothing else.
Example:
1. Research topic
2. Create outline
3. Write first draft"""
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=300,
        )
        
        response_text = message.choices[0].message.content
        subtasks = [
            line.strip() 
            for line in response_text.split('\n') 
            if line.strip() and line[0].isdigit()
        ]
        
        # Remove numbering (e.g., "1. Task" → "Task")
        subtasks = [s.split('. ', 1)[1] if '. ' in s else s for s in subtasks]
        
        return subtasks if subtasks else [task_title]
    
    except Exception as e:
        print(f"❌ Error breaking down task: {e}")
        return [task_title]


def get_motivation(task_title: str) -> str:
    """
    Get a motivational message for a task
    """
    try:
        message = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""Give ONE punchy, funny but genuine motivational message for someone about to do this task: {task_title}

Keep it under 15 words. No preamble. Just the message."""
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.8,
            max_tokens=100,
        )
        
        return message.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"❌ Error getting motivation: {e}")
        return "You've got this! Just start now. 💪"


def generate_reminder(task_title: str) -> str:
    """
    Generate a gentle reminder to complete a task
    """
    try:
        message = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""Create a gentle but firm reminder for someone about: {task_title}

Be understanding. They might be procrastinating. One sentence."""
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=100,
        )
        
        return message.choices[0].message.content.strip()
    
    except Exception as e:
        print(f"❌ Error generating reminder: {e}")
        return f"Don't forget: {task_title} is waiting for you! Go get it. 🚀"


def check_groq_connection() -> bool:
    """
    Test if Groq API is accessible
    """
    if not GROQ_API_KEY:
        return False
    
    try:
        message = client.chat.completions.create(
            messages=[{"role": "user", "content": "Say 'ok'"}],
            model="mixtral-8x7b-32768",
            max_tokens=10,
        )
        return True
    except Exception as e:
        print(f"❌ Groq connection failed: {e}")
        return False
