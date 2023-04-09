from aiogram.filters.base import Filter
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, CallbackQuery

from loader import admins
from keyboards.callbacks import AdminTaskCallback, TaskCompletingCallback
from database import Database, TaskStatus


class IsAdminFilter(Filter):
    def __init__(self, is_admin: bool) -> None:
        self.is_admin = is_admin

    async def __call__(self, message: Message) -> bool:
        return (str(message.from_user.id) in admins) == self.is_admin


class AdminTaskStatusFilter(Filter):
    def __init__(self, *args):
        self.statuses = args

    async def __call__(self, callback_query: CallbackQuery) -> bool:
        db = Database()
        data = AdminTaskCallback.unpack(callback_query.data)
        status = await db.get_task_status(data.task_id)
        return status in self.statuses


class TaskCompletingStatusFilter(Filter):
    def __init__(self, *args):
        self.statuses = args

    async def __call__(self, callback_query: CallbackQuery) -> bool:
        db = Database()
        data = TaskCompletingCallback.unpack(callback_query.data)
        status = await db.get_task_status(data.task_id)
        return status in self.statuses
