from aiogram.filters.base import Filter
from aiogram.types import Message, CallbackQuery

from loader import admins
from utils.shift import Shift
from keyboards.callbacks import AdminPrintTaskCallback,\
    PrintTaskCompletingCallback, AdminScanTaskCallback
from database import Database


class IsAdminFilter(Filter):
    def __init__(self, is_admin: bool) -> None:
        self.is_admin = is_admin

    async def __call__(self, message: Message) -> bool:
        return (message.from_user.id in admins) == self.is_admin


class IsAnyAdminsOnShiftFilter(Filter):
    def __init__(self, flag: bool) -> None:
        self.flag = flag

    async def __call__(self, message: Message) -> bool:
        return (True if len(Shift.get_active()) else False) == self.flag


class AdminPrintTaskStatusFilter(Filter):
    def __init__(self, *args):
        self.statuses = args

    async def __call__(self, callback_query: CallbackQuery, *args) -> bool:
        db = Database()
        data = AdminPrintTaskCallback.unpack(callback_query.data)
        status = await db.get_task_status(data.task_id)
        return status in self.statuses


class AdminScanTaskStatusFilter(Filter):
    def __init__(self, *args):
        self.statuses = args

    async def __call__(self, callback_query: CallbackQuery, *args) -> bool:
        db = Database()
        data = AdminScanTaskCallback.unpack(callback_query.data)
        status = await db.get_task_status(data.task_id)
        return status in self.statuses


class TaskCompletingStatusFilter(Filter):
    def __init__(self, *args):
        self.statuses = args

    async def __call__(self, callback_query: CallbackQuery, *args) -> bool:
        db = Database()
        data = PrintTaskCompletingCallback.unpack(callback_query.data)
        status = await db.get_task_status(data.task_id)
        return status in self.statuses
