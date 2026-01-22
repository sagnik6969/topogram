# 1. Import IndexModel and sorting constants from pymongo
from pymongo import IndexModel, ASCENDING

from beanie import Document
from pydantic import Field
from datetime import datetime


class UserThread(Document):
    user_id: str
    thread_id: str
    title: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "user_threads"
        indexes = [
            IndexModel([("user_id", ASCENDING), ("thread_id", ASCENDING)], unique=True)
        ]
