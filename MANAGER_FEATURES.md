# 👔 Manager Mode - Feature Documentation

## Overview

Manager Mode transforms DOIT into an AI-powered project manager that tracks your progress, enforces deadlines, and keeps you accountable. Think of it as having a supportive PM watching your back.

---

## Features

### 1. **Task Status Tracking** 📋

Every task has 4 states:

```
not_started  →  in_progress  →  completed
                    ↓
                  blocked
```

| Status | Meaning | Example |
|--------|---------|---------|
| **not_started** | Task hasn't begun yet | New task added |
| **in_progress** | Actively working on it | Started writing code |
| **blocked** | Stuck, needs help | Waiting for someone's input |
| **completed** | Done! ✅ | Shipped to production |

### 2. **Progress Tracking** 📊

Each task shows 0-100% progress:
- 0% = Haven't started
- 25% = Started exploring
- 50% = Mid-way through
- 75% = Almost there
- 100% = Complete!

Manager asks: *"What % done is this?"*

### 3. **Deadline Management** ⏰

Set deadlines and the manager warns you:

**3+ days before:** 📅 Reminder  
**1-3 days:** ⏰ URGENT - Get moving!  
**Overdue:** 🚨 CRITICAL - Do this NOW!

---

## Backend API Endpoints

### Manager Endpoints

#### Get Manager View
```bash
GET /api/manager/tasks/{user_id}
```

Returns:
```json
{
  "overdue": [...],
  "due_soon": [...],
  "in_progress": [...],
  "blocked": [...],
  "completed": [...],
  "stats": {
    "total": 10,
    "completed": 3,
    "in_progress": 4,
    "blocked": 1,
    "overdue": 2
  }
}
```

#### Get Deadline Warnings
```bash
GET /api/manager/warnings/{user_id}
```

Returns:
```json
{
  "urgent_warnings": 2,
  "warnings": [
    {
      "task_id": "123",
      "task_title": "Submit report",
      "days_remaining": -1,
      "warning": "🚨 OVERDUE by 1 day. This needs your attention NOW.",
      "is_overdue": true
    }
  ]
}
```

#### Request Progress Update
```bash
POST /api/manager/request-update
```

Body:
```json
{
  "user_id": "user-1",
  "task_id": "task-123"
}
```

Response:
```json
{
  "message": "📋 How's 'Design landing page' coming? It's been 2 days since we last checked.",
  "reminder_count": 1
}
```

#### Update Task Status
```bash
PUT /api/manager/task-update/{task_id}
```

Body:
```json
{
  "user_id": "user-1",
  "status": "in_progress",
  "progress": "50"
}
```

Response:
```json
{
  "manager_feedback": "✨ Great start! You're at 50%. Keep the momentum!",
  "task_updated": {
    "status": "in_progress",
    "progress": "50"
  }
}
```

#### Generate Progress Report
```bash
GET /api/manager/progress-report/{user_id}
```

Returns:
```json
{
  "report": "📊 Solid week! You've completed 60% of your tasks. The blocked items need attention - let's unblock them tomorrow.",
  "stats": {
    "total_tasks": 10,
    "completed": 6,
    "in_progress": 3,
    "blocked": 1,
    "completion_rate": "60%"
  }
}
```

#### Weekly Standup
```bash
GET /api/manager/weekly-standup/{user_id}
```

Returns:
```json
{
  "standup": "🎯 Great week ahead! Let's crush the 5 tasks on our plate. I'm here if you get stuck.",
  "generated_at": "2026-04-01T10:00:00"
}
```

---

## React Components

### Manager Component

Main component showing manager dashboard.

**Props:**
- `userId` (string) - User ID to track tasks

**Tabs:**
1. **Overview** - All tasks organized by status
2. **Deadlines** - Urgent warnings and deadlines
3. **Report** - Weekly progress report

**Features:**
- Real-time stats cards
- AI manager standup message
- Task grouping by urgency
- One-click report generation
- Auto-refresh every 30 minutes

### Usage

```jsx
import Manager from './components/Manager'

export default function App() {
  return <Manager userId="user-123" />
}
```

---

## Database Schema Updates

### Tasks Table - New Fields

```python
status = Column(String)              # not_started, in_progress, blocked, completed
due_date = Column(DateTime)          # Deadline for task
progress_percentage = Column(String)  # 0-100%
last_status_update = Column(DateTime)# When was last update
manager_reminder_count = Column(String) # How many reminders sent
```

---

## AI Integration

The Manager uses **Groq API** to:

1. **Generate deadline warnings** - Natural, conversational urgency messages
2. **Request updates** - Personalized progress check-ins
3. **Provide feedback** - Encouragement and guidance
4. **Generate reports** - Weekly summaries with insights
5. **Weekly standups** - Motivational kickoff messages

### Example AI Responses

**Deadline Warning:**
```
⏰ "Design landing page" is due tomorrow! Let's get this shipped. 💪
```

**Progress Request:**
```
📋 Status check: How's 'API Integration' looking? Haven't heard from you in 2 days.
```

**Manager Feedback:**
```
✨ Awesome work! You're 75% through this task. Just one more sprint and we're done!
```

---

## User Workflow

### Day 1: Set Up Tasks
1. Create tasks in regular Task Board
2. Add deadlines and priorities
3. Switch to Manager Mode

### Day 2-4: Track Progress
1. Manager shows Overview of all tasks
2. Click on task → Update status/progress
3. Get AI feedback for each update

### Day 5: Deadline Warnings
1. Manager highlights overdue/due-soon tasks
2. AI generates urgent warnings
3. You prioritize accordingly

### Week End: Review Report
1. Manager generates progress report
2. Shows completion rate and insights
3. Weekly standup for next week

---

## Notification Strategy

Manager asks for updates when:

- ⏰ **3 days until deadline** - First gentle reminder
- ⏰ **1 day until deadline** - URGENT warning
- 🚨 **Overdue** - Critical message
- 📋 **No update in 2+ days** - "How's it going?" check-in

Example flow:
```
Day 1: Task created, due April 10
Day 7 (April 7): 3-day reminder sent
Day 9 (April 9): 1-day urgent warning
Day 10 (April 10): OVERDUE alert
Day 11+: Daily critical reminders
```

---

## Settings (Future)

These will be configurable:

```json
{
  "reminder_frequency": "daily",  // daily, weekly, when_urgent
  "deadline_warnings": "3",        // Days before deadline
  "manager_tone": "supportive",    // supportive, strict, funny
  "auto_status_update": true,      // Auto-advance based on time
  "weekly_report_day": "friday"   // When to generate report
}
```

---

## Example: Complete Manager Flow

### Step 1: Add Task with Deadline
```
Title: "Launch v2.0 API"
Due Date: April 15
Priority: HIGH
```

### Step 2: AI Manager Response
Standup: *"🎯 Exciting! Let's launch that API. Clear your calendar and ship it!"*

### Step 3: Start Working (Day 1-2)
Update: Status = `in_progress`, Progress = `50%`
AI Feedback: *"💪 Great momentum! Keep pushing!"*

### Step 4: Hit Blocker (Day 3)
Update: Status = `blocked`, Progress = `60%`
AI Message: *"⚠️ Blocked? Let's solve this. What's the issue?"*

### Step 5: Unblock (Day 4)
Update: Status = `in_progress`, Progress = `85%`
AI: *"✨ Nice! Almost there. Just the polish left!"*

### Step 6: Complete (Day 5)
Update: Status = `completed`, Progress = `100%`
AI: *"🎉 SHIPPED! Amazing work. Let's celebrate!"*

### Step 7: Weekly Report
*"📊 Fantastic week! You shipped the API on time. 90% completion rate - that's excellence. 3 more features and we're golden!"*

---

## Configuration (backend/.env)

```
# Already set up:
GROQ_API_KEY=your_key
DATABASE_URL=postgresql://...

# Future:
MANAGER_REMINDER_DAYS=3
MANAGER_TONE=supportive
```

---

## Testing the Manager

### In Development

1. Start backend: `python backend/main.py`
2. Go to `http://localhost:8000/docs`
3. Test endpoints:
   - GET `/api/manager/tasks/{user_id}`
   - POST `/api/manager/request-update`
   - GET `/api/manager/progress-report/{user_id}`

### In React UI

1. Click **👔 Manager Mode** in navbar
2. See dashboard with all tasks
3. Try updating task status
4. Generate progress report

---

## Future Features

- 🔔 Email/Slack notifications
- 📈 Performance trending
- 🎯 SMART goal setting
- 💬 Chat with manager
- 📱 Mobile app
- 📊 Team-level reports
- ⚡ Automated status based on time spent
- 🤖 ML-powered deadline predictions

---

## Technical Stack

**Frontend:**
- React components
- Real-time updates
- Tab-based UI

**Backend:**
- FastAPI endpoints
- PostgreSQL queries
- Groq AI integration

**Database:**
- 6 new fields on tasks table
- Priority + deadline indexes
- AIResponse logging table

---

## Troubleshooting

### No data showing in Manager
→ Check backend is running: `http://localhost:8000/docs`

### AI responses not generating
→ Verify GROQ_API_KEY in backend/.env

### Deadlines not showing warnings
→ Make sure due_date is set on tasks

### Progress not updating
→ Check PUT endpoint is returning correct status

---

## That's the Manager Mode! 🎉

Your app just became a full project manager. Keep shipping! 🚀
