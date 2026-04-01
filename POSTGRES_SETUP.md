# PostgreSQL Installation Quick Reference

## What You Need to Install

✅ **PostgreSQL** - The database system  
✅ **Python packages** - Already listed in `requirements.txt`  
✅ **Groq API key** - Free from groq.com

That's it! No other applications needed.

---

## Installation by OS

### 🍎 macOS - Easiest

```bash
# Install Homebrew first (if you don't have it)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install PostgreSQL
brew install postgresql@15

# Start it (runs in background)
brew services start postgresql@15

# Verify it works
psql --version
```

Once installed:
```bash
# Create your database (one time only)
createdb doit_db

# Later, if needed: restart PostgreSQL
brew services restart postgresql@15
```

### 🪟 Windows - Need to Download

1. Visit: https://www.postgresql.org/download/windows/
2. Download PostgreSQL 15 installer
3. Run `.exe` file
4. During install:
   - **Port**: Keep as 5432 (default)
   - **Password**: Save this! You'll need it in `.env`
   - **Superuser**: postgres (default)
5. Finish install

Then test:
```bash
# Open PowerShell and type:
psql -U postgres -d doit_db
# Type the password you set
# You should see: doit_db=#
```

### 🐧 Linux - Ubuntu/Debian

```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Start service
sudo systemctl start postgresql

# Create database
sudo -u postgres createdb doit_db

# Verify
sudo -u postgres psql doit_db
```

---

## What PostgreSQL Does

```
Your App  →  PostgreSQL  →  Data stored on disk
React/Python   (Server)
```

PostgreSQL is a "server" that listens on port 5432 and stores your data safely.

---

## Verify Installation (All OS)

Open terminal and type:
```bash
psql --version
```

Should show something like:
```
psql (PostgreSQL) 15.0
```

---

## Connection String Explained

```
postgresql://username:password@host:port/database_name
```

Example:
```
postgresql://postgres:mypassword@localhost:5432/doit_db
  └─ user      └─ password  └─ host      └─ port └─ database
```

- **User**: `postgres` (default)
- **Password**: What you set during install
- **Host**: `localhost` (your computer)
- **Port**: `5432` (default, don't change)
- **Database**: `doit_db` (we create this)

---

## File You Modified

After installing, update `backend/.env`:

```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/doit_db
GROQ_API_KEY=your_groq_key
```

Replace `YOUR_PASSWORD` with password you set during PostgreSQL install.

---

## Commands You'll Use

```bash
# Check if PostgreSQL is running
psql --version

# Connect to database
psql -U postgres -d doit_db

# Inside psql shell:
\l              # List all databases
\c doit_db      # Connect to specific database
\dt             # List all tables
\q              # Exit

# Terminal commands:
createdb mydb   # Create database
dropdb mydb     # Delete database
```

---

## Next Steps

1. Install PostgreSQL ✅
2. Update `.env` with credentials ✅
3. Run `python backend/init_db.py` → Creates tables
4. Start backend: `python backend/main.py`
5. Test at `http://localhost:8000/docs`

---

## Don't Worry About

❌ Learning SQL (you don't need to!)  
❌ Advanced PostgreSQL setup  
❌ Performance tuning yet  
❌ User authentication (for now)

The Python code handles all of that automatically.

---

## Where to Put Your Password

Only in these 2 places:
1. `backend/.env` ← Production  
2. `backend/.env` ← Development

**NEVER** commit `.env` to GitHub (already in `.gitignore`)

---

**Ready? Start with your OS above and let me know when PostgreSQL is installed!** 🚀
