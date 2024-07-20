import uuid
from datetime import datetime
from typing import List, Dict, Any

import jwt
from fastapi import Request, HTTPException, status
from jwt import PyJWTError
from sqlalchemy import select

from apps.config import SECRET_KEY, ALGORITHM
from apps.database import new_session
from apps.models import Task
from apps.schemas import TaskGetSchema, TaskCreateSchema


class TaskService:
    @classmethod
    async def get_tasks_by_user_id(cls, user_id: uuid.uuid4) -> List[TaskGetSchema]:
        async with new_session() as session:
            query = select(Task).filter(Task.user_id == user_id)
            result = await session.execute(query)
            tasks = result.scalars().all()
            tasks_schemas = [TaskGetSchema.model_validate(task) for task in tasks]
            return tasks_schemas

    @classmethod
    async def get_task_by_id(cls, task_id: uuid.uuid4) -> TaskGetSchema:
        async with new_session() as session:
            query = select(Task).filter(Task.id == task_id)
            result = await session.execute(query)
            task = result.scalars().first()
            task_schema = TaskGetSchema.model_validate(task)
            return task_schema

    @classmethod
    async def create_task(cls, user_id: uuid.uuid4, data: TaskCreateSchema) -> None:
        async with new_session() as session:
            data_dict = data.model_dump()
            due_datetime = datetime.strptime(data_dict['due_datetime'], '%Y-%m-%d %H:%M:%S')
            data_dict['due_datetime'] = due_datetime
            task = Task(**data_dict)
            task.user_id = user_id
            session.add(task)
            await session.commit()
            return None


class TokenService:
    @classmethod
    def get_token_from_cookie(cls, request: Request) -> str:
        token = request.cookies.get('access_token')
        if token:
            return token
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Token not found in cookies'
        )

    @classmethod
    def decode_token(cls, token: str) -> Dict[str, Any]:
        try:
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return decoded_token
        except PyJWTError:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
