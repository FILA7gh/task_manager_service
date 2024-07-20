import uuid

from sqlalchemy import Column, String, Boolean, UUID, Text, DateTime

from apps.database import Base


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    due_datetime = Column(DateTime, nullable=True)
    is_executed = Column(Boolean, default=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
