from dataclasses import dataclass
from enum import Enum
import aiosqlite
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

    async def close_database(self) -> None:
        await self.conn.close()

    async def finish_task_creation(self, task: Task) -> None:
        cursor = \
            await self.conn.execute(
                "UPDATE tasks SET task_type=?, file_path=?, number_of_copies=?,"
                " coast=?, sides_count=?, pay_way=?, "
                "status=? WHERE id=?",
                (task.task_type.value, task.file_path,
                 task.number_of_copies, task.coast,
                 task.sides_count.value, task.pay_way.value,
                 task.status.value, task.id_))
        await self.conn.commit()
        await cursor.close()

    async def get_new_id(self) -> int:
        cursor = await self.conn.execute("SELECT MAX(id) FROM tasks")
        result = (await cursor.fetchone())[0]
        await cursor.close()
        print(result)
        return (result if result is not None else -1) + 1

    async def create_new_task(self, user_id: int) -> int:
        id_ = await self.get_new_id()
        cursor = await self.conn.execute("INSERT INTO tasks (id, user_id, "
                                         "status) VALUES (?, ?, ?)",
                                         (id_, user_id,
                                          TaskStatus.CREATION.value))
        await self.conn.commit()
        await cursor.close()
        return id_

    async def update_task_status(self, id_: int, new_status: TaskStatus) -> None:
        cursor = await self.conn.execute("UPDATE tasks SET status=? WHERE "
                                         "id=?", (new_status.value, id_))
        await self.conn.commit()
        await cursor.close()

    async def get_task_status(self, id_: int) -> TaskStatus:
        cursor = await self.conn.execute("SELECT status FROM tasks WHERE "
                                         "id=?", (id_, ))
        result = (await cursor.fetchone())[0]
        await cursor.close()
        return TaskStatus(result)

    async def get_user_id_by_task_id(self, id_: int) -> int:
        cursor = await self.conn.execute("""SELECT user_id FROM tasks WHERE \
                                            id=?""", (id_, ))
        result = (await cursor.fetchone())[0]
        await cursor.close()
        return result

    async def get_task(self, id_: int) -> Task:
        cursor = await self.conn.execute("""SELECT * FROM tasks WHERE id=?""",
                                         (id_, ))
        result = (await cursor.fetchone())
        return Task(*result)


async def main():
    await Database().init_database()
    # await Database().create_new_task(123)
    # task = Task(0, 200, TaskType.PRINT_TASK, "1.pdf", 1, 5,
    # SidesCount.ONE, PayWay.CARD, TaskStatus.PENDING)
    # await Database().finish_task_creation(task)
    # print(await Database().create_new_task())
    print(await Database().get_task(16))
    await Database().close_database()


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
