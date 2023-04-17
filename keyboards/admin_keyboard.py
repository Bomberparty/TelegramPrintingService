from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.callbacks import AdminPrintTaskCallback, Actions, \
    PrintTaskCompletingCallback, AdminScanTaskCallback


def get_print_task_keyboard(id_: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Разрешить печать",
                                     callback_data=AdminPrintTaskCallback(action=Actions.ACCEPT, task_id=id_).pack()))
    builder.add(InlineKeyboardButton(text="Отмена",
                                     callback_data=AdminPrintTaskCallback(action=Actions.CANCEL, task_id=id_).pack()))
    return builder.as_markup()


def get_scan_task_keyboard(id_: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Начать сканирование",
                                     callback_data=AdminScanTaskCallback(action=Actions.ACCEPT, task_id=id_).pack()))
    builder.add(InlineKeyboardButton(text="Отмена",
                                     callback_data=AdminScanTaskCallback(action=Actions.CANCEL, task_id=id_).pack()))
    return builder.as_markup()


def get_print_completing_task_keyboard(id_: int) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Печать успешно закончилась",
                                     callback_data=PrintTaskCompletingCallback(action=Actions.ACCEPT, task_id=id_).pack()))
    builder.add(InlineKeyboardButton(text="Печать провалилась",
                                     callback_data=PrintTaskCompletingCallback(action=Actions.CANCEL, task_id=id_).pack()))
    return builder.as_markup()
