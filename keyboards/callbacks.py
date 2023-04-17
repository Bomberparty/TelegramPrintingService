from aiogram.filters.callback_data import CallbackData

from enum import Enum, IntEnum


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
