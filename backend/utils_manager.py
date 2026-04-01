"""
Manager AI - Acts like a PM/Manager tracking progress
"""

import os
from groq import Groq
from datetime import datetime, timedelta

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print("⚠️  Warning: GROQ_API_KEY not set in .env")

client = Groq(api_key=GROQ_API_KEY)

def get_deadline_warning(task_title: str, due_date: str, days_remaining: int) -> str:
    """
    Generate a deadline warning from manager perspective
    """
    try:
        urgency = "URGENT" if days_remaining <= 1 else "OVERDUE" if days_remaining < 0 else "REMINDER"
        
        message = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a supportive but no-nonsense project manager. 
Generate a short deadline warning for this task.

Task: {task_title}
Due: {due_date}
Days remaining: {days_remaining}
Urgency: {urgency}

Keep it to 1-2 sentences. Be direct but not harsh. Include emoji."""
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=100,
        )
        
        return message.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error generating deadline warning: {e}")
        return f"⏰ Deadline coming up for '{task_title}' on {due_date}"


def request_progress_update(task_title: str, status: str, last_update_days_ago: int) -> str:
    """
    Manager asking for progress update
    """
    try:
        message = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a friendly project manager checking in on team progress.
Ask for a status update on this task. Be encouraging but professional.

Task: {task_title}
Current Status: {status}
Last update: {last_update_days_ago} days ago

Keep it to 1-2 sentences. Include emoji.
Examples: "What's the status?" "How's progress looking?" etc"""
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.8,
            max_tokens=100,
        )
        
        return message.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error requesting progress: {e}")
        return f"📋 Status check: How's '{task_title}' coming along?"


def generate_progress_report(tasks_data: list) -> str:
    """
    Generate a comprehensive progress report
    
    tasks_data = [
        {"title": "Task 1", "status": "in_progress", "progress": 50},
        ...
    ]
    """
    try:
        # Format tasks for the prompt
        tasks_summary = "\n".join([
            f"- {t['title']}: {t['status']} ({t.get('progress', 0)}% done)"
            for t in tasks_data[:10]  # Limit to 10 tasks
        ])
        
        message = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a project manager generating a weekly progress report.
Analyze this task list and create a brief but insightful summary.

Tasks:
{tasks_summary}

Generate a 3-4 sentence report that:
1. Shows overall progress
2. Highlights blockers/issues
3. Gives encouragement
4. Suggests one thing to focus on

Be professional but friendly. Include emojis."""
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.7,
            max_tokens=200,
        )
        
        return message.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        return "📊 Progress Report: Keep pushing! 💪"


def get_manager_feedback(task_title: str, status: str, progress: str) -> str:
    """
    Get personalized manager feedback
    """
    try:
        message = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a supportive project manager giving feedback.

Task: {task_title}
Status: {status}
Progress: {progress}%

Give 1-2 sentences of feedback:
- If stuck: offer help
- If in progress: encourage continuation
- If complete: celebrate it
- If not started: nudge to begin

Include emoji. Be genuine and motivating."""
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.8,
            max_tokens=100,
        )
        
        return message.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error getting feedback: {e}")
        return f"✨ You've got this! Keep working on {task_title}."


def get_weekly_standup(tasks_data: list) -> str:
    """
    Generate manager's weekly standup message
    """
    try:
        task_count = len(tasks_data)
        completed_count = len([t for t in tasks_data if t['status'] == 'completed'])
        in_progress_count = len([t for t in tasks_data if t['status'] == 'in_progress'])
        blocked_count = len([t for t in tasks_data if t['status'] == 'blocked'])
        
        message = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"""You are a project manager doing a weekly standup.

Stats:
- Total tasks: {task_count}
- Completed: {completed_count}
- In Progress: {in_progress_count}
- Blocked: {blocked_count}

Generate a standup message that:
1. Acknowledges the progress
2. Addresses any blockers
3. Sets tone for the week

Keep it 2-3 sentences, professional but encouraging. Include emojis.
Examples: "Nice work!" "Let's tackle blockers" "Another great week ahead"etc"""
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.8,
            max_tokens=150,
        )
        
        return message.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Error generating standup: {e}")
        return f"📊 Weekly Standup: {completed_count}/{task_count} tasks done. Great progress! 💪"
