from typing import TypeVar

from returns.context import ReaderFutureResultE
from returns.future import FutureSuccess, future_safe

from todo_fp.domains import Todo
from todo_fp.repositories import TodoRepository
from todo_fp.schemas import TodoAddSchema
from todo_fp.uow import UnitOfWork

_T = TypeVar("_T")


def _transaction(instance: _T) -> ReaderFutureResultE[None, UnitOfWork]:
    return (
        ReaderFutureResultE[..., UnitOfWork]
        .ask()
        .bind_future_result(lambda uow: future_safe(uow.session.commit)())
        .bind_future_result(lambda _: FutureSuccess(instance))
    )


class TodoService:
    @staticmethod
    def get_all_todos() -> ReaderFutureResultE[list[Todo], UnitOfWork]:
        return ReaderFutureResultE.from_value(...).bind(TodoRepository.get_all)

    @staticmethod
    def add_todo(schema: TodoAddSchema) -> ReaderFutureResultE[Todo, UnitOfWork]:
        return (
            ReaderFutureResultE.from_value(schema)
            .map(Todo.from_add_dto)
            .bind_context_ioresult(TodoRepository.add)
            .bind(_transaction)
        )
