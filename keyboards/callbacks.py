from aiogram.filters.callback_data import CallbackData

from enum import Enum


class Actions(Enum):
    CANCEL = 0
    ACCEPT = 1


class AdminTaskCallback(CallbackData):
    action: Actions
    task_id: str
