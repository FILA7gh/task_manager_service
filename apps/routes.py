from fastapi import Depends, Path, status, Request
from fastapi.encoders import jsonable_encoder
from fastapi.routing import APIRouter
from typing import Annotated, List

from pydantic import UUID4
from starlette.responses import JSONResponse

from apps.services import TaskService, TokenService
from apps.schemas import TaskCreateSchema, TaskGetSchema

task_router = APIRouter(prefix='/tasks', tags=['tasks routers'])


@task_router.get('', response_model=List[TaskGetSchema])
async def get_tasks(request: Request) -> JSONResponse:
    token_data = TokenService.decode_token(TokenService.get_token_from_cookie(request))
    user_id = token_data['user_id']
    tasks = await TaskService.get_tasks_by_user_id(user_id)
    tasks_json = jsonable_encoder(tasks)
    response = JSONResponse(content={'data': tasks_json}, status_code=status.HTTP_200_OK)
    return response


@task_router.get('/{task_id}', response_model=TaskGetSchema)
async def get_task_by_id(task_id: Annotated[UUID4, Path()]) -> JSONResponse:
    task = await TaskService.get_task_by_id(task_id)
    task_json = jsonable_encoder(task)
    response = JSONResponse(content={'data': task_json}, status_code=status.HTTP_200_OK)
    return response


@task_router.post('', response_model=dict)
async def create_task(request: Request, data: Annotated[TaskCreateSchema, Depends()],) -> JSONResponse:
    token_data = TokenService.decode_token(TokenService.get_token_from_cookie(request))
    user_id = token_data['user_id']
    await TaskService.create_task(user_id, data)
    response = JSONResponse(content={'message': 'task created successfully'}, status_code=status.HTTP_201_CREATED)
    return response
