from dataclasses import dataclass
from uuid import UUID, uuid4

from todo_fp.dtos import TodoAddDto


@dataclass
class Todo:
    id_: UUID
    title: str
    is_finished: bool

    @classmethod
    def from_add_dto(cls, dto: TodoAddDto) -> "Todo":
        return cls(id_=uuid4(), title=dto.title, is_finished=False)
