import random


class Database:
    async def dispose(self):
        ...


class AsyncSession:
    def __init__(self, bind: Database):
        ...

    def add(self, *args):
        ...

    async def commit(self, *args):
        if random.random() < 0.5:
            raise ValueError("Error occured during committing")

    async def rollback(self):
        ...

    async def close(self):
        ...
