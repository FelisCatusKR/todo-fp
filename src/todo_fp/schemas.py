from pydantic.dataclasses import dataclass


@dataclass(frozen=True)
class TodoAddSchema:
    title: str
