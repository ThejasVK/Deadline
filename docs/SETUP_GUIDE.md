# Setup Guide - Learn While Building

This guide will walk you through setting up DOIT and integrating each part of the tech stack.

## Step 1: Initial Setup ✅ DONE

You now have:
- React + Vite project structure
- Basic UI components (Hero, Navigation, TaskBoard)
- Design system with your color palette
- Environment configuration

### What to do now:
```bash
npm install
npm run dev
```

You should see the app running at `http://localhost:3000` with:
- Navigation bar with "DOIT." branding
- Hero section with catchy copy
- Task board UI with add/filter functionality

---

## Step 2: Connect to Supabase (NEXT)

### What you'll learn:
- How to set up a Supabase project
- Create database tables
- Use Supabase client in React
- Real authentication

### Tasks:
1. Go to [supabase.com](https://supabase.com)
2. Create a new project (free tier)
3. Get your `API URL` and `anon key`
4. Create two tables:
   - `users` (auto-created by auth)
   - `tasks` table with fields:
     - `id` (uuid, primary key)
     - `user_id` (uuid, foreign key to auth.users)
     - `title` (text)
     - `description` (text)
     - `category` (text)
     - `priority` (text: high/medium/low)
     - `completed` (boolean)
     - `created_at` (timestamp)
     - `updated_at` (timestamp)

5. Update `.env.local` with your credentials
6. Replace local state in `TaskBoard.jsx` with Supabase queries

### Example code you'll modify:

Replace:
```jsx
const [tasks, setTasks] = useState([...])
```

With:
```jsx
const [tasks, setTasks] = useState([])

useEffect(() => {
  const fetchTasks = async () => {
    const data = await getTasks(userId)
    setTasks(data)
  }
  fetchTasks()
}, [userId])
```

---

## Step 3: Ollama Integration

### What you'll learn:
- Local AI/ML model setup
- API calls to Ollama
- Streaming responses

### Setup Ollama:
1. Install from [ollama.ai](https://ollama.ai)
2. Download a model: `ollama pull llama2`
3. Run: `ollama serve`
4. Verify: `curl http://localhost:11434/api/tags`

### What to add:
- Button on TaskCard: "Break down this task"
- Click it → calls `breakDownTask()` from utils
- Show subtasks

---

## Step 4: User Authentication

### What you'll learn:
- User signup/login flows
- Protected routes
- Session management

### Create pages:
- `pages/Login.jsx`
- `pages/Signup.jsx`
- `pages/Dashboard.jsx`

### Use Supabase Auth:
```jsx
import { supabase } from '@/utils/supabase'

const signUp = async (email, password) => {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
  })
  return { data, error }
}
```

---

## Step 5: Deploy to Vercel

### What you'll learn:
- CI/CD pipelines
- Environment management
- Production deployment

### Steps:
1. Push to GitHub
2. Connect repo to Vercel
3. Set environment variables
4. Deploy!

---

## Learning Goals by Feature

### React Concepts You'll Use:
- ✅ Components & Props
- ✅ State with `useState`
- ✅ Side effects with `useEffect`
- ⏳ Context API (for user data)
- ⏳ Custom hooks

### Supabase Concepts:
- ⏳ SQL Basics
- ⏳ Row Level Security (RLS)
- ⏳ Real-time subscriptions
- ⏳ JWT authentication

### Ollama/AI Concepts:
- ⏳ REST API calls
- ⏳ Streaming responses
- ⏳ Prompt engineering
- ⏳ Error handling

### Deployment:
- ⏳ Environment variables
- ⏳ Build optimization
- ⏳ Monitoring

---

## Quick Reference: Key Files to Modify

| Step | Files | What to Do |
|------|-------|-----------|
| 1 | `src/App.jsx`, `src/components/` | ✅ Done - UI structure |
| 2 | `src/utils/supabase.js`, `.env.local`, `src/components/TaskBoard.jsx` | Connect database |
| 3 | `src/utils/ollama.js`, `src/components/TaskCard.jsx` | Add AI features |
| 4 | `src/pages/Login.jsx`, `src/components/Navigation.jsx` | Add auth |
| 5 | `vercel.json`, GitHub settings | Deploy |

---

## Troubleshooting

### `npm install` fails
- Make sure Node 16+ is installed: `node --version`
- Delete `node_modules` and `package-lock.json`, then reinstall

### App doesn't start
- Check port 3000 is available
- Try: `npm run dev -- --port 3001`

### Supabase connection fails
- Verify `.env.local` has correct URL and key
- Check network access isn't blocked
- Test with Supabase dashboard directly

### Ollama errors
- Make sure it's running: `curl http://localhost:11434/api/tags`
- Try pulling a model: `ollama pull llama2`
- Check `.env.local` has correct URL

---

## Need Help?

- React: [react.dev](https://react.dev) - official docs
- Supabase: [supabase.com/docs](https://supabase.com/docs)
- Ollama: [ollama.ai](https://ollama.ai)
- Vite: [vitejs.dev](https://vitejs.dev)

Good luck! You've got this. 🚀
