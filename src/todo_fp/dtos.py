from dataclasses import dataclass


@dataclass(frozen=True)
class TodoAddDto:
    title: str
