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


@dataclass
class Task:
    _id: int
    task_type: TaskType
    file_name: str
    number_of_copies: int
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

    async def init_database(self):
        self.conn = await aiosqlite.connect(dbname)
        await self.conn.execute(f'''CREATE TABLE IF NOT EXISTS tasks(
        id INTEGER PRIMARY KEY,
        task_type INTEGER,
        file_name TEXT,
        number_of_copies INTEGER, 
        sides_count TEXT,
        pay_way INTEGER,
        status INTEGER
        )''')
        await self.conn.commit()

    async def close_database(self):
        await self.conn.close()

    async def create_task(self, task: Task):
        await self.conn.execute(f"INSERT INTO tasks (id, task_type, file_name,"
                                f" number_of_copies, sides_count, pay_way,"
                                f" status) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (task._id,
                                 task.task_type.value, task.file_name,
                                 task.number_of_copies,
                                 task.sides_count.value, task.pay_way.value,
                                 task.status.value))
        await self.conn.commit()


async def main():
    await Database().init_database()
    task = Task(1, TaskType.PRINT_TASK, "1.pdf", 1,
                SidesCount.ONE, PayWay.CARD,
                TaskStatus.PENDING)

    await Database().create_task(task)
    await Database().close_database()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
