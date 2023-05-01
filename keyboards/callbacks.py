from aiogram.filters.callback_data import CallbackData
from enum import Enum, IntEnum

from database import TaskType


class Actions(IntEnum):
    CANCEL = 0
    ACCEPT = 1


class AdminPrintTaskCallback(CallbackData, prefix="admin_print"):
    action: Actions
    task_id: int


class PrintTaskCompletingCallback(CallbackData, prefix="print_completing"):
    action: Actions
    task_id: int


class AdminScanTaskCallback(CallbackData, prefix="admin_scan"):
    action: Actions
    task_id: int


class ScanningCallback(CallbackData, prefix="scanning"):
    action: Actions
    task_id: int
    index: int


class CardCallback(CallbackData, prefix="card"):
    action: Actions
    id_: int
    task_type: TaskType
    task_id: int
