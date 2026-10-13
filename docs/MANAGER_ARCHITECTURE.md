# Manager Mode Architecture & Flow

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         USER INTERACTION LAYER                       │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Task Board                          Manager Dashboard               │
│  ├─ Add task                         ├─ View all tasks by urgency   │
│  ├─ Set deadline                     ├─ See deadline warnings       │
│  ├─ Update progress                  ├─ Get progress reports        │
│  └─ Mark complete                    └─ Read AI standup             │
│                                                                       │
├─────────────────────────────────────────────────────────────────────┤
│                         REACT FRONTEND                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Components:                         API Calls:                      │
│  • Manager.jsx                       GET  /api/manager/tasks        │
│  • TaskBoard.jsx                     POST /api/manager/request-    │
│  • Navigation.jsx                           update                  │
│  • TaskCard.jsx                      PUT  /api/manager/task-       │
│                                            update                   │
│                          ↕ HTTP Requests ↕                          │
│                                                                       │
├─────────────────────────────────────────────────────────────────────┤
│                      PYTHON FASTAPI BACKEND                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Routes (routes_manager.py):          Utilities (utils_manager.py):  │
│  • GET /manager/tasks                 • get_deadline_warning()       │
│  • GET /manager/warnings              • request_progress_update()    │
│  • POST /manager/request-update       • generate_progress_report()   │
│  • PUT /manager/task-update           • get_manager_feedback()       │
│  • GET /manager/progress-report       • get_weekly_standup()         │
│  • GET /manager/weekly-standup                                       │
│                                                                       │
│                          ↕ Database Queries ↕                       │
│                                                                       │
├─────────────────────────────────────────────────────────────────────┤
│                     GROQ AI INTEGRATION                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  • Break down tasks                  • Generate deadlines            │
│  • Create warnings                   • Provide feedback              │
│  • Request updates                   • Write standup messages        │
│                                                                       │
│                          ↕ API Calls ↕                              │
│                                                                       │
├─────────────────────────────────────────────────────────────────────┤
│                 PostgreSQL DATABASE                                  │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  tasks table:                                                        │
│  ├─ id, user_id, title, description                                │
│  ├─ status (not_started, in_progress, blocked, completed)          │
│  ├─ priority, category                                             │
│  ├─ due_date (deadline)                                            │
│  ├─ progress_percentage (0-100%)                                   │
│  ├─ last_status_update (when user last updated)                    │
│  ├─ manager_reminder_count (how many times manager asked)          │
│  └─ created_at, updated_at                                         │
│                                                                       │
│  Indexes:                                                            │
│  • idx_user_status (fast filtering by status)                      │
│  • idx_due_date (fast deadline queries)                            │
│                                                                       │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Data Flow: Task Status Update

### When user clicks "Mark In Progress"

```
1. React Component (TaskCard.jsx)
   └─ User clicks "Update Status"
      └─ Calls: updateTaskStatus(userId, taskId, "in_progress", 50)

2. React Makes API Call
   └─ PUT /api/manager/task-update/task-123
      └─ Body: {user_id: "user-1", status: "in_progress", progress: "50"}

3. FastAPI Backend (routes_manager.py)
   └─ Receives request at update_task_status()
      └─ Queries database for task

4. Database (PostgreSQL)
   └─ Updates task row:
      ├─ status = "in_progress"
      ├─ progress_percentage = "50"
      ├─ last_status_update = NOW()
      └─ updated_at = NOW()

5. Manager AI (utils_manager.py)
   └─ Calls: get_manager_feedback(title, status, progress)
      └─ Sends to Groq API with prompt

6. Groq AI API
   └─ Generates response:
      "✨ Great start! You're at 50%. Keep this momentum!"

7. Backend Returns Response
   └─ {
       "success": true,
       "manager_feedback": "✨ Great start! You're at 50%. Keep this momentum!",
       "task_updated": {status: "in_progress", progress: "50"}
      }

8. React Receives & Displays
   └─ Shows feedback message to user
      └─ Manager: "✨ Great start! You're at 50%. Keep this momentum!"
```

---

## Deadline Warning Flow

### When user opens Manager dashboard

```
1. React Component Mounts (Manager.jsx)
   └─ useEffect calls fetchManagerData()

2. API Call 1: Get Manager View
   └─ GET /api/manager/tasks/user-1
      └─ Backend queries all tasks for user
         ├─ Categorizes by status
         ├─ Checks due dates vs NOW()
         └─ Returns organized task list

3. API Call 2: Get Warnings
   └─ GET /api/manager/warnings/user-1
      └─ Backend finds tasks with due_date <= 3 days away
         └─ For each task:
            ├─ Calculate days remaining
            ├─ Call get_deadline_warning() (AI)
            ├─ Groq generates warning message
            └─ Add to warnings list

4. Groq AI Generates Warnings
   └─ Prompt: "You are a PM. Generate deadline warning for task 'Design API' due in 1 day. Be supportive but urgent."
      └─ Response: "⏰ 'Design API' due TOMORROW! Final push - you've got this! 💪"

5. React Displays Dashboard
   └─ Shows:
      ├─ Overdue tasks (red)
      ├─ Due soon tasks (orange)
      ├─ In progress (blue)
      ├─ Blocked (pink)
      └─ Completed (green)
```

---

## Weekly Report Generation Flow

### When user clicks "Generate Report"

```
1. User Clicks Button
   └─ Button: <Generate Report/>

2. React Makes API Call
   └─ GET /api/manager/progress-report/user-1

3. Backend (routes_manager.py)
   └─ Queries all tasks for user
      └─ Extracts:
         ├─ title
         ├─ status
         ├─ progress_percentage
         └─ Creates tasks_data list

4. Manager AI (utils_manager.py)
   └─ Calls generate_progress_report(tasks_data)
      └─ Formats tasks into readable format
      └─ Sends to Groq with prompt:
         "Generate a 3-4 sentence progress report showing:
          1. Overall progress
          2. Blockers
          3. Encouragement
          4. One focus area"

5. Groq Generates Report
   └─ "📊 Solid progress! You've completed 7/10 tasks (70%). 
       The 2 blocked items need attention - let's unblock them tomorrow.
       Excellent momentum overall. Focus on those blockers next week!"

6. Backend Calculates Stats
   └─ ├─ Total: 10
      ├─ Completed: 7
      ├─ Completion rate: 70%
      └─ In progress: 2
         Blocked: 1

7. React Receives Full Response
   └─ {
       "report": "📊 Solid progress!...",
       "stats": {
         "total_tasks": 10,
         "completed": 7,
         "completion_rate": "70%"
       }
      }

8. React Displays Report Card
   └─ Shows:
      ├─ Report text
      ├─ Statistics grid
      └─ Refresh button
```

---

## Manager Decision Tree

### When to show what warnings

```
for each task in user_tasks:
  
  if task.status == "completed":
    → Show in "Completed - Great Work!" ✅
  
  elif task.status == "blocked":
    → Show in "Blocked - Need Help" 🚫
    → Generate: "What's blocking this? Let me help!"
  
  elif task.status == "in_progress":
    if task.due_date:
      days_left = (due_date - now()).days
      
      if days_left < 0:
        → Show in "OVERDUE" section 🚨
        → Generate: "CRITICAL: This is overdue by {days_left} days!"
      
      elif days_left <= 1:
        → Show in "Due Soon" with ⏰ 
        → Generate: "URGENT: Due TOMORROW!"
      
      elif days_left <= 3:
        → Show in "Due Soon" with ⏰
        → Generate: "Reminder: Due in {days_left} days"
    
    else:
      → Show in "In Progress" 🔄
      → No warning (no deadline)
  
  elif task.status == "not_started":
    if task.due_date:
      days_left = (due_date - now()).days
      
      if days_left < 0:
        → URGENT: "This is overdue! Start NOW!"
      
      elif days_left <= 1:
        → "Not started but due TOMORROW? 😅 Time to begin!"
      
      elif days_left <= 3:
        → "Not started - only {days_left} days left!"
    
    else:
      → Show in regular "Not Started" (no rush)
  
  # For all in_progress tasks:
  if (now - task.last_status_update) > 2_days:
    → Send message: "How's {task} coming? Checking in on progress."
```

---

## API Response Patterns

### Pattern 1: Success Response with Data

```python
{
  "success": true,
  "data": {
    "key": "value"
  }
}
```

### Pattern 2: Manager Feedback Response

```python
{
  "success": true,
  "manager_feedback": "Your AI manager message",
  "current_status": "in_progress",
  "current_progress": "50"
}
```

### Pattern 3: Multiple Categories Response

```python
{
  "success": true,
  "data": {
    "overdue": [...],
    "due_soon": [...],
    "in_progress": [...],
    "blocked": [...],
    "completed": [...],
    "stats": {
      "total": 10,
      "completed": 3,
      ...
    }
  }
}
```

---

## Component Communication

```
App.jsx
├─ state: showManager, userId
│
├─> Navigation.jsx
│   └─ onManagerClick() → toggles showManager
│
└─> Conditional Render:
    ├─ if showManager:
    │  └─ <Manager userId={userId} />
    │     ├─ Fetches: /api/manager/tasks
    │     ├─ Fetches: /api/manager/warnings
    │     ├─ Tabs: Overview, Deadlines, Report
    │     └─ Children: TaskGroup (display tasks)
    │
    └─ if !showManager:
       └─ <TaskBoard userId={userId} />
          ├─ state: tasks, newTask, filter
          ├─ Add/Edit tasks
          ├─ Children: TaskCard (individual tasks)
          └─ Calls: API to update tasks
```

---

## Database Query Examples

### Get all overdue tasks

```sql
SELECT * FROM tasks 
WHERE user_id = 'user-1' 
  AND due_date < NOW() 
  AND status != 'completed'
ORDER BY due_date ASC;
```

### Get tasks due soon

```sql
SELECT * FROM tasks 
WHERE user_id = 'user-1' 
  AND due_date BETWEEN NOW() AND NOW() + INTERVAL '3 days'
  AND status != 'completed'
ORDER BY due_date ASC;
```

### Get manager statistics

```sql
SELECT 
  COUNT(*) as total,
  SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
  SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress,
  SUM(CASE WHEN status = 'blocked' THEN 1 ELSE 0 END) as blocked,
  SUM(CASE WHEN status != 'completed' AND due_date < NOW() THEN 1 ELSE 0 END) as overdue
FROM tasks 
WHERE user_id = 'user-1';
```

---

## Performance Optimizations

### Current

- ✅ Database indexes on: user_id, status, due_date
- ✅ Pagination on warning retrieval (limit 50)
- ✅ Frontend caching (30-minute refresh interval)

### Future

- ⏳ Add Redis caching layer
- ⏳ Batch AI requests (send 5 warnings at once)
- ⏳ Lazy load report generation
- ⏳ WebSocket for real-time updates
- ⏳ Queue system for AI calls

---

## Error Handling

### Try/Catch in Backend Routes

```python
@app.get("/api/manager/tasks/{user_id}")
async def get_manager_view(user_id: str):
  try:
    tasks = query_tasks(user_id)  # May fail
    process_tasks(tasks)          # May fail
    return {"success": true, "data": organized_tasks}
  
  except HTTPException:
    raise  # Re-raise HTTP errors
  
  except Exception as e:
    raise HTTPException(status_code=500, detail=str(e))
```

---

## Future Enhancements

### Phase 2: Real-Time Updates
- WebSocket connection
- Live dashboard updates
- Instant feedback

### Phase 3: Notifications
- Email reminders
- Slack integration
- Push notifications

### Phase 4: Analytics
- Productivity trends
- Completion patterns
- Bottleneck identification

### Phase 5: Collaboration
- Team tasks
- Shared deadlines
- Manager notifications

---

## Summary

The Manager system is built on:

1. **Clear separation of concerns:**
   - Frontend (React) = UI
   - Backend (FastAPI) = Logic
   - Database (PostgreSQL) = State
   - AI (Groq) = Intelligence

2. **Status-driven categorization** of tasks

3. **Deadline-triggered warnings** with AI generation

4. **Progress tracking** with automated feedback

5. **Comprehensive reporting** with insights

6. **Scalable architecture** ready for notifications, real-time updates, and team features

This is a production-ready system. Ship it! 🚀
