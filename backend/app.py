from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uuid

tasks_db = {}

app = FastAPI(title="DOIT API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"status": "DOIT API Running", "v": "0.1.0"}

@app.get("/health")
async def health():
    return {"ok": True}

@app.get("/api/tasks/")
async def get_tasks(user_id: str = "default"):
    return {"success": True, "data": tasks_db.get(user_id, [])}

@app.post("/api/tasks/")
async def create_task(user_id: str = "default", title: str = ""):
    task = {"id": str(uuid.uuid4()), "title": title, "completed": False}
    if user_id not in tasks_db:
        tasks_db[user_id] = []
    tasks_db[user_id].append(task)
    return {"success": True, "data": task}

@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str, user_id: str = "default"):
    if user_id in tasks_db:
        tasks_db[user_id] = [t for t in tasks_db[user_id] if t["id"] != task_id]
    return {"success": True}

@app.put("/api/tasks/{task_id}")
async def update_task(task_id: str, user_id: str = "default", completed: bool = None):
    if user_id in tasks_db:
        for task in tasks_db[user_id]:
            if task["id"] == task_id and completed is not None:
                task["completed"] = completed
    return {"success": True}

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 DOIT Backend Ready!\n📍 http://localhost:8000\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)
