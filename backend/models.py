from database import Base
from sqlalchemy import Column, String, Boolean, DateTime, Text, Index
from datetime import datetime
import uuid

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String, default="medium")  # high, medium, low
    status = Column(String, default="not_started")  # not_started, in_progress, blocked, completed
    completed = Column(Boolean, default=False, index=True)
    category = Column(String, default="work")  # work, health, personal, etc
    due_date = Column(DateTime, nullable=True, index=True)  # Deadline for task
    progress_percentage = Column(String, default="0")  # 0-100%
    last_status_update = Column(DateTime, nullable=True)  # When was last update
    manager_reminder_count = Column(String, default="0")  # How many times manager asked for update
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Indexes for common queries
    __table_args__ = (
        Index('idx_user_completed', 'user_id', 'completed'),
        Index('idx_user_priority', 'user_id', 'priority'),
        Index('idx_user_status', 'user_id', 'status'),
        Index('idx_due_date', 'due_date'),
    )

class AIResponse(Base):
    __tablename__ = "ai_responses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    user_id = Column(String, index=True, nullable=False)
    task_id = Column(String, nullable=False)
    prompt = Column(Text, nullable=False)
    response = Column(Text, nullable=False)
    ai_model = Column(String, default="mixtral-8x7b-32768")
    created_at = Column(DateTime, default=datetime.utcnow)
