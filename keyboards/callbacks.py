from aiogram.filters.callback_data import CallbackData

from enum import Enum, IntEnum


class Actions(IntEnum):
    CANCEL = 0
    ACCEPT = 1


class AdminTaskCallback(CallbackData, prefix="admin_task"):
    action: Actions
    task_id: int


class TaskCompletingCallback(CallbackData, prefix="task_completing"):
    action: Actions
    task_id: int
