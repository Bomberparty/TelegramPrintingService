from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.callbacks import AdminTaskCallback, Actions, TaskCompletingCallback


async def get_task_keyboard(id_: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Разрешить печать",
                                     callback_data=AdminTaskCallback(action=Actions.ACCEPT, task_id=id_).pack()))
    builder.add(InlineKeyboardButton(text="Отмена",
                                     callback_data=AdminTaskCallback(action=Actions.CANCEL, task_id=id_).pack()))
    return builder.as_markup()


async def get_completing_task_keyboard(id_: int) -> InlineKeyboardMarkup:

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Печать успешно закончилась",
                                     callback_data=TaskCompletingCallback(action=Actions.ACCEPT, task_id=id_).pack()))
    builder.add(InlineKeyboardButton(text="Печать не закончилась",
                                     callback_data=TaskCompletingCallback(action=Actions.CANCEL, task_id=id_).pack()))
    return builder.as_markup()
