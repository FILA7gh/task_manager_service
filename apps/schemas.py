import datetime

from pydantic import BaseModel, UUID4, ConfigDict


class TaskGetSchema(BaseModel):
    id: UUID4
    title: str
    description: str
    due_datetime: datetime.datetime
    is_executed: bool
    user_id: UUID4

    model_config = ConfigDict(from_attributes=True)


class TaskCreateSchema(BaseModel):
    title: str
    description: str
    due_datetime: str


class TaskExecuteSchema(BaseModel):
    is_executed: bool
