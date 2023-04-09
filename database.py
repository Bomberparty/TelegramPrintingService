from dataclasses import dataclass
from enum import Enum
import aiosqlite

import loader
from loader import dbname


class TaskType(Enum):
    PRINT_TASK = 0
    SCAN_TASK = 1


class SidesCount(Enum):
    ONE = "one-sided"
    TWO = "two-sided-long-edge"


class PayWay(Enum):
    CARD = 0
    CASH = 1


class TaskStatus(Enum):
    CREATION = 0
    CONFIRMING = 1
    PENDING = 2
    FINISHED = 3
    CANCELED = 4
    FAILED = 5


@dataclass
class Task:
    id_: int
    user_id: int
    task_type: TaskType
    file_path: str
    number_of_copies: int
    coast: int
    sides_count: SidesCount
    pay_way: PayWay
    status: TaskStatus

    def __post_init__(self):
        #Нужно изменить этот костыль
        if isinstance(self.task_type, int):
            self.task_type = TaskType(self.task_type)
        if isinstance(self.sides_count, str):
            self.sides_count = SidesCount(self.sides_count)
        if isinstance(self.pay_way, str):
            self.pay_way = PayWay(self.pay_way)
        if isinstance(self.status, str):
            self.status = TaskStatus(self.status)


def database_connect(func):
    async def wrapper(*args, **kwargs):
        async with aiosqlite.connect(loader.dbname) as conn:
            return await func(*args, **kwargs, conn=conn)

    return wrapper


class Database:
    """ Создаётся таблица с параметрами заказа
    Параметр confirmed отвечает за подтверждение заказа админом
    Рекомендуется проверять сначала confirmed, а затем pending"""

    _instance = None
    conn = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @database_connect
    async def finish_task_creation(self, task: Task, conn) -> None:
        cursor = \
            await conn.execute(
                "UPDATE tasks SET task_type=?, file_path=?, number_of_copies=?,"
                " coast=?, sides_count=?, pay_way=?, "
                "status=? WHERE id=?",
                (task.task_type.value, task.file_path,
                 task.number_of_copies, task.coast,
                 task.sides_count.value, task.pay_way.value,
                 task.status.value, task.id_))
        await conn.commit()
        await cursor.close()

    @database_connect
    async def get_new_id(self, conn) -> int:
        cursor = await conn.execute("SELECT MAX(id) FROM tasks")
        result = (await cursor.fetchone())[0]
        await cursor.close()
        return (result if result is not None else -1) + 1

    @database_connect
    async def create_new_task(self, user_id: int, conn) -> int:
        id_ = await self.get_new_id()
        cursor = await conn.execute("INSERT INTO tasks (id, user_id, "
                                    "status) VALUES (?, ?, ?)",
                                    (id_, user_id,
                                     TaskStatus.CREATION.value))
        await conn.commit()
        await cursor.close()
        return id_

    @database_connect
    async def update_task_status(self, id_: int, new_status: TaskStatus,
                                 conn) -> None:
        cursor = await conn.execute("UPDATE tasks SET status=? WHERE "
                                    "id=?", (new_status.value, id_))
        await conn.commit()
        await cursor.close()

    @database_connect
    async def get_task_status(self, id_: int, conn) -> TaskStatus:
        cursor = await conn.execute("SELECT status FROM tasks WHERE "
                                    "id=?", (id_,))
        result = (await cursor.fetchone())[0]
        await cursor.close()
        return TaskStatus(result)

    @database_connect
    async def get_user_id_by_task_id(self, id_: int, conn) -> int:
        cursor = await conn.execute("""SELECT user_id FROM tasks WHERE \
                                            id=?""", (id_,))
        result = (await cursor.fetchone())[0]
        await cursor.close()
        return result

    @database_connect
    async def get_task(self, id_: int, conn) -> Task:
        cursor = await conn.execute("""SELECT * FROM tasks WHERE id=?""",
                                    (id_,))
        result = (await cursor.fetchone())
        return Task(*result)

async def main():
    # await Database().init_database()
    await Database().create_new_task(123)
    # task = Task(0, 200, TaskType.PRINT_TASK, "1.pdf", 1, 5,
    # SidesCount.ONE, PayWay.CARD, TaskStatus.PENDING)
    # await Database().finish_task_creation(task)
    # print(await Database().create_new_task())
    print(await Database().get_task(16))


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
