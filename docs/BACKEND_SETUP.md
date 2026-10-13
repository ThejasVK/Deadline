# DOIT Backend Setup Guide

## Prerequisites

- Python 3.9+
- PostgreSQL (local or cloud)
- Groq API key (free from console.groq.com)

---

## Step 1: Install PostgreSQL

### Option A: Local Installation (Recommended for Learning)

#### macOS
```bash
# Install PostgreSQL
brew install postgresql@15

# Start service
brew services start postgresql@15

# Create database
createdb doit_db

# Verify connection
psql -U postgres -d doit_db
```

#### Windows
1. Download from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run installer
3. Remember the password you set
4. Keep port as 5432

Test:
```bash
psql -U postgres -d doit_db
```

#### Linux
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo -u postgres createdb doit_db
```

### Option B: Cloud Database (Recommended for Production)

Use [Railway](https://railway.app) - Create free PostgreSQL in 2 minutes

---

## Step 2: Get Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up (free)
3. Create API key
4. Copy it

---

## Step 3: Install Backend Dependencies

```bash
# Go to backend folder
cd backend

# Create virtual environment
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

---

## Step 4: Configure Environment

Edit `backend/.env`:

```
DATABASE_URL=postgresql://postgres:password@localhost:5432/doit_db
GROQ_API_KEY=your_key_from_groq
ENVIRONMENT=development
PORT=8000
```

---

## Step 5: Initialize Database

```bash
# Create tables
python init_db.py

# Expected output:
# 🔄 Creating database tables...
# ✅ Database initialized successfully!
# 📋 Tables created:
#    - users
#    - tasks
#    - ai_responses
```

---

## Step 6: Start Backend Server

```bash
python main.py

# Expected output:
# 🚀 DOIT. Backend Starting...
# 📍 Server: http://localhost:8000
# 📚 Docs: http://localhost:8000/docs
```

---

## Test Your Backend

### Using FastAPI Docs (Interactive)

Visit: **http://localhost:8000/docs**

You'll see all API endpoints you can test:
- GET `/api/tasks/` - Get user tasks
- POST `/api/tasks/` - Create task
- POST `/api/ai/break-down` - Break task into steps

### Test with curl

```bash
# Get health status
curl http://localhost:8000/health

# Create a task
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-1",
    "title": "Learn Python",
    "priority": "high"
  }'
```

---

## Troubleshooting

### Error: "Could not connect to database"

**Check 1:** PostgreSQL is running
```bash
# macOS
brew services list

# Linux
sudo systemctl status postgresql
```

**Check 2:** DATABASE_URL is correct
```
# Wrong:
DATABASE_URL=postgresql://root:@localhost:5432/doit

# Right:
DATABASE_URL=postgresql://postgres:password@localhost:5432/doit_db
```

**Check 3:** Database exists
```bash
psql -U postgres -l  # List all databases
```

### Error: "Could not import FastAPI"

```bash
# Reinstall packages
pip install --upgrade -r requirements.txt
```

### Error: "GROQ_API_KEY not found"

- Check `.env` file exists in `backend/` folder
- Check you copied the key correctly from console.groq.com
- Verify no extra spaces

---

## API Endpoints

### Base URL
```
http://localhost:8000
```

### Tasks

```
GET    /api/tasks/                    - Get all tasks
POST   /api/tasks/                    - Create task
PUT    /api/tasks/{task_id}           - Update task
DELETE /api/tasks/{task_id}           - Delete task
GET    /api/tasks/stats/{user_id}     - Get statistics
```

### AI

```
GET    /api/ai/health                 - Check Groq connection
POST   /api/ai/break-down             - Break task into steps
POST   /api/ai/motivation             - Get motivation
POST   /api/ai/reminder               - Get reminder
```

---

## Database Structure

### tasks table
```
- id (UUID)
- user_id (String)
- title (String)
- description (Text, optional)
- priority (high/medium/low)
- completed (Boolean)
- category (work/health/personal)
- created_at (DateTime)
- updated_at (DateTime)
```

### Indexes (for fast queries)
```
- user_id
- completed
- priority
- user_id + completed
- user_id + priority
```

---

## Next: Connect Frontend

Update React to call this API:

```javascript
// src/utils/api.js
const API_URL = 'http://localhost:8000'

export const getTasks = async (userId) => {
  const response = await fetch(`${API_URL}/api/tasks/?user_id=${userId}`)
  return response.json()
}
```

---

## Deployment

Ready to deploy? See `DEPLOYMENT.md` (coming soon)

---

## Need Help?

- Backend errors: Check `backend.log`
- Database issues: Use `psql` to inspect
- API issues: Go to `http://localhost:8000/docs` to test

Good luck! 🚀
