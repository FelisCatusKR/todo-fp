from uuid import UUID

from returns.context import ReaderFutureResultE, ReaderIOResultE
from returns.functions import tap
from returns.future import FutureResultE, FutureSuccess
from returns.io import IOResult, IOResultE, impure_safe

from todo_fp.domains import Todo
from todo_fp.uow import UnitOfWork

_repo = {
    UUID(int=0x00000000000040008000000000000000): Todo(
        id_=UUID(int=0x00000000000040008000000000000000),
        title="test1",
        is_finished=False,
    )
}


def _add(todo: Todo):
    _repo[todo.id_] = todo


class TodoRepository:
    @staticmethod
    def get_all(*args) -> ReaderFutureResultE[list[Todo], UnitOfWork]:
        def func(uow: UnitOfWork) -> FutureResultE[list[Todo]]:
            return FutureSuccess([todo for todo in _repo.values()])

        return ReaderFutureResultE(func)

    @staticmethod
    def add(todo: Todo) -> ReaderIOResultE[Todo, UnitOfWork]:
        def func(uow: UnitOfWork) -> IOResultE[Todo]:
            return (
                IOResult.from_value(todo)
                .map(tap(_add))
                .bind(impure_safe(tap(uow.session.add)))
            )

        return ReaderIOResultE(func)
