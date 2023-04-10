from dataclasses import dataclass

from todo_fp.adapters import AsyncSession


@dataclass(frozen=True)
class UnitOfWork:
    session: AsyncSession
