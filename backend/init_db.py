"""
Initialize the database - creates all tables
Run this once: python init_db.py
"""

from database import engine, Base
from models import Task, User, AIResponse

def init_db():
    print("🔄 Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized successfully!")
    print("\n📋 Tables created:")
    print("   - users")
    print("   - tasks")
    print("   - ai_responses")

if __name__ == "__main__":
    init_db()
