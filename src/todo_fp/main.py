from contextlib import asynccontextmanager
from dataclasses import asdict
from typing import Annotated

from fastapi import Depends, FastAPI
from returns.io import IOFailure, IOSuccess
from returns.unsafe import unsafe_perform_io

from todo_fp.adapters import AsyncSession, Database
from todo_fp.schemas import TodoAddSchema
from todo_fp.services import TodoService
from todo_fp.uow import UnitOfWork

database = Database()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await database.dispose()


app = FastAPI(lifespan=lifespan)


async def get_uow():
    uow = UnitOfWork(session=AsyncSession(bind=database))
    try:
        yield uow
    finally:
        await uow.session.rollback()
        await uow.session.close()


@app.get("/todos")
async def get_todos(uow: Annotated[UnitOfWork, Depends(get_uow)]):
    result = await TodoService.get_all_todos()(uow).awaitable()
    return [schema for schema in map(asdict, unsafe_perform_io(result.unwrap()))]


@app.post("/todos")
async def add_todo(schema: TodoAddSchema, uow: Annotated[UnitOfWork, Depends(get_uow)]):
    result = await TodoService.add_todo(schema)(uow).awaitable()
    match result:
        case IOFailure(e):
            return {"error": unsafe_perform_io(e)}
        case IOSuccess(value):
            return asdict(unsafe_perform_io(value))
