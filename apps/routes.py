from fastapi import Depends, status, Request, Response
from fastapi.routing import APIRouter
from typing import Annotated, List

from pydantic import UUID4
from starlette.responses import JSONResponse

from apps.services import TaskService, TokenService
from apps.schemas import TaskCreateSchema, TaskGetSchema, TaskExecuteSchema

task_router = APIRouter(prefix='/tasks', tags=['tasks routers'])


@task_router.get('', response_model=List[TaskGetSchema])
async def get_tasks(request: Request) -> List[TaskGetSchema]:
    token_data = TokenService.decode_token(TokenService.get_token_from_cookie(request))
    user_id = token_data['user_id']
    tasks = await TaskService.get_tasks_by_user_id(user_id)
    return tasks


@task_router.get('/{task_id}', response_model=TaskGetSchema, status_code=status.HTTP_200_OK)
async def get_task_by_id(task_id: UUID4) -> TaskGetSchema:
    task = await TaskService.get_task_by_id(task_id)
    return task


@task_router.post('')
async def create_task(request: Request, data: Annotated[TaskCreateSchema, Depends()],) -> JSONResponse:
    token_data = TokenService.decode_token(TokenService.get_token_from_cookie(request))
    user_id = token_data['user_id']
    await TaskService.create_task(user_id, data)
    response = JSONResponse(content={'message': 'task created successfully'}, status_code=status.HTTP_201_CREATED)
    return response


@task_router.put('/{task_id}')
async def update_task(task_id: UUID4, task_status: Annotated[TaskExecuteSchema, Depends()]) -> JSONResponse:
    await TaskService.update_task_status(task_id, task_status)
    return JSONResponse(content={'message': 'Task status updated'}, status_code=status.HTTP_200_OK)


@task_router.delete('/{task_id}')
async def delete_task(task_id: UUID4) -> Response:
    await TaskService.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
