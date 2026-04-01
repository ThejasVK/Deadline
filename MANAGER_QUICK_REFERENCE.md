# 👔 Manager Mode - Quick Reference Guide

## What You Now Have

Your DOIT app now includes **an AI manager that**:
- 📊 Tracks all task statuses and progress
- ⏰ Sends deadline warnings and reminders
- 💬 Provides personalized AI feedback
- 📈 Generates progress reports
- 🎯 Gives weekly standups
- 🚨 Alerts on overdue tasks

---

## Quick Start (5 minutes)

### 1. Start Backend
```bash
cd backend
python main.py
```

### 2. Open React App
```bash
# In another terminal
npm run dev
```

### 3. Click Manager Mode
```
Navigation bar → Click 👔 Manager Mode
```

### 4. See the Dashboard
- Stats cards showing task breakdown
- AI standup message
- Tasks organized by urgency
- Deadline warnings (if any)

---

## New Features at a Glance

| Feature | Where | What It Does |
|---------|-------|------------|
| **Task Status** | TaskBoard | Track: not_started → in_progress → blocked → completed |
| **Deadline Tracking** | Task Details | Set due dates, get warnings 3/1/0 days before |
| **Progress %** | TaskBoard | Show 0-100% progress on each task |
| **Manager Dashboard** | Manager Mode | See all tasks organized by urgency |
| **Deadline Warnings** | Manager Tab 1 | Get AI-generated urgency messages |
| **Progress Report** | Manager Tab 2 | Generate weekly summary with insights |
| **Weekly Standup** | Manager Header | AI kickoff message for motivation |
| **Manager Feedback** | On Update | Get encouraging AI response when you update status |

---

## Files Modified/Created

### New Backend Files
- `backend/utils_manager.py` - AI manager brain
- `backend/routes_manager.py` - Manager API endpoints

### New Frontend Files
- `src/components/Manager.jsx` - Manager dashboard
- `src/styles/Manager.css` - Beautiful styling

### Updated Backend Files
- `backend/models.py` - (added 5 new fields to Task)
- `backend/main.py` - (added manager routes)

### Updated Frontend Files
- `src/App.jsx` - (added manager toggle logic)
- `src/components/Navigation.jsx` - (added Manager Mode button)
- `src/components/TaskBoard.jsx` - (added userId prop)

### Documentation Added
- `MANAGER_FEATURES.md` - Complete feature docs
- `MANAGER_MODE_SUMMARY.md` - Implementation summary
- `MANAGER_ARCHITECTURE.md` - System architecture
- `MANAGER_QUICK_REFERENCE.md` - This file!

---

## Task Fields (Database)

Every task now has:

```
status: "in_progress"              ← Current state
due_date: "2026-04-15"             ← Deadline
progress_percentage: "50"           ← How far done (0-100%)
last_status_update: "2026-04-01"   ← When last updated
manager_reminder_count: "2"         ← Manager's reminder count
```

---

## Usage Scenarios

### Scenario 1: Weekly Planning
```
1. Create 5 tasks for the week
2. Set deadlines for each
3. Click "👔 Manager Mode"
4. Read standup message for motivation
5. Get organized view of whole week
```

### Scenario 2: Task Execution
```
1. Start task → Update status to "in_progress"
2. Progress to 50% → Get: "💪 Halfway there!"
3. Progress to 100% → Get: "🎉 SHIPPED!"
```

### Scenario 3: Deadline Alert
```
1. Create task due tomorrow
2. Manager shows: "⏰ DUE TOMORROW - Final push!"
3. Can't miss it - it's right there!
```

### Scenario 4: Weekly Review
```
1. End of week, click "Generate Report"
2. Get insights on completion rate
3. See what was blocked
4. Plan better for next week
```

---

## AI Responses Examples

### Deadline Warning (3 days before)
```
📅 "API Integration" due in 3 days. Time to get started! 🚀
```

### Deadline Warning (1 day before)
```
⏰ URGENT: "API Integration" due TOMORROW! Final push - you've got this! 💪
```

### Deadline Warning (Overdue)
```
🚨 CRITICAL: "API Integration" is 2 days OVERDUE. This needs immediate attention!
```

### Progress Request (no update in 2 days)
```
📋 Status check: How's "API Integration" coming? Haven't heard in 2 days.
```

### Feedback on Progress Update
```
✨ Great start! You're at 50%. Keep this momentum going!
```

### Feedback on Completion
```
🎉 SHIPPED! Amazing work on "API Integration". Celebrate this win! 🎊
```

### Weekly Report
```
📊 Fantastic week! 8/10 tasks completed (80%). The 2 blocked items need attention. 
Keep this pace - you're crushing it! 🚀
```

---

## API Endpoints Reference

### Get Manager Dashboard
```
GET /api/manager/tasks/{user_id}
```
Returns: All tasks organized by urgency

### Get Deadline Warnings
```
GET /api/manager/warnings/{user_id}
```
Returns: List of urgent deadline warnings

### Request Status Update
```
POST /api/manager/request-update?user_id={user_id}&task_id={task_id}
```
Returns: Manager's "how's it going?" message

### Update Task Status
```
PUT /api/manager/task-update/{task_id}
Body: {user_id, status, progress}
```
Returns: Manager's feedback on the update

### Generate Progress Report
```
GET /api/manager/progress-report/{user_id}
```
Returns: Weekly summary + stats

### Get Weekly Standup
```
GET /api/manager/weekly-standup/{user_id}
```
Returns: Motivational kickoff message

---

## Testing Checklist

- [ ] Backend runs: `python main.py`
- [ ] Frontend runs: `npm run dev`
- [ ] Click "👔 Manager Mode" button appears
- [ ] Manager dashboard loads
- [ ] Stats cards show (Total, Completed, In Progress, etc)
- [ ] Standup message displays
- [ ] Can see Overview/Deadlines/Report tabs
- [ ] Create task with deadline
- [ ] Task appears in Manager view
- [ ] Update task status → Get feedback
- [ ] Generate report → See stats

---

## Common Tasks

### Create Task with Deadline
```
1. Task Board → Add task
2. Title: "Launch API v2"
3. Due Date: Pick date (e.g., April 15)
4. Priority: HIGH
5. Done!
```

### Check Deadlines
```
1. Click "👔 Manager Mode"
2. Click "⏰ Deadlines" tab
3. See all tasks with warnings
```

### Update Progress
```
1. Task Board → Find task
2. Click task → Update status
3. Set progress (e.g., 50%)
4. Get manager feedback instantly
```

### Get Weekly Report
```
1. Manager Mode → Click "📊 Report" tab
2. Click "Generate Report" button
3. Wait for AI to generate
4. See stats and insights
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Manager button not showing | Refresh page in browser |
| Dashboard shows "Loading..." | Check backend is running |
| No tasks in dashboard | Make sure tasks have user_id matching yours |
| AI responses not generating | Check GROQ_API_KEY in backend/.env |
| Deadline warnings empty | Create task with due_date set |
| API errors | Check http://localhost:8000/docs for details |

---

## Next Steps

### Immediate
- ✅ Try Manager Mode dashboard
- ✅ Create task with deadline
- ✅ Update progress and get feedback
- ✅ Generate weekly report

### Soon (Next Session)
- Connect React frontend to Python API for real database persistence
- Add email/Slack notifications
- Real-time dashboard updates

### Later
- Mobile notifications
- Team collaboration features
- Performance analytics
- Custom manager personalities

---

## Key Concepts

### Task Lifecycle
```
created → not_started → in_progress → completed
                            ↓
                           blocked (optional)
```

### Deadline System
```
+3 days: 📅 Reminder
+1 day:  ⏰ URGENT
0 days:  🚨 OVERDUE
-1 day+: 🚨 CRITICAL
```

### Progress Reporting
```
0-30%:  Just getting started
30-60%: Making good progress
60-90%: Almost there!
90-100%: Done! 🎉
```

---

## Architecture in 30 Seconds

```
User → React UI → Python API → AI (Groq) → Database (PostgreSQL)
                ↓                               ↓
         Manager Dashboard      Tasks + Status + Deadlines
```

---

## Still Have Questions?

📚 Read these docs (in order):
1. `MANAGER_MODE_SUMMARY.md` - Overview
2. `MANAGER_FEATURES.md` - Detailed features
3. `MANAGER_ARCHITECTURE.md` - Technical deep dive

---

## You're All Set! 🚀

Your DOIT app is now:
- ✅ Task management system
- ✅ Deadline tracker
- ✅ Progress reporter
- ✅ AI accountability partner
- ✅ Productivity tool

**Go build great things!** 💪

---

## Cheat Sheet

```
# Start everything
Backend: python backend/main.py
Frontend: npm run dev

# Access
Frontend: http://localhost:3000
API Docs: http://localhost:8000/docs

# Quick Actions
👔 Manager Mode → See dashboard
📊 Generate Report → Get weekly summary
⏰ Deadlines tab → Check upcoming
🔄 Update task → Get feedback
```

Good luck! You've built something amazing. 🎉
