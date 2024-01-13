from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from keyboards.callbacks import (
    AdminPrintTaskCallback,
    Actions,
    PrintTaskCompletingCallback,
    AdminScanTaskCallback,
    ScanningCallback,
)


def get_print_task_keyboard(id_: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Разрешить печать",
            callback_data=AdminPrintTaskCallback(
                action=Actions.ACCEPT, task_id=id_
            ).pack(),
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="Отмена",
            callback_data=AdminPrintTaskCallback(
                action=Actions.CANCEL, task_id=id_
            ).pack(),
        )
    )
    return builder.as_markup()


def get_scan_task_keyboard(id_: int) -> InlineKeyboardMarkup:
    """ВЫдаёт клавиатуру с началом сканирования"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Начать сканирование",
            callback_data=AdminScanTaskCallback(
                action=Actions.ACCEPT, task_id=id_
            ).pack(),
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="Отмена",
            callback_data=AdminScanTaskCallback(
                action=Actions.CANCEL, task_id=id_
            ).pack(),
        )
    )
    return builder.as_markup()


def get_print_completing_task_keyboard(id_: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Печать успешно закончилась",
            callback_data=PrintTaskCompletingCallback(
                action=Actions.ACCEPT, task_id=id_
            ).pack(),
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="Печать провалилась",
            callback_data=PrintTaskCompletingCallback(
                action=Actions.CANCEL, task_id=id_
            ).pack(),
        )
    )
    return builder.as_markup()


def get_scanning_keyboard(id_: int, index: int) -> InlineKeyboardMarkup:
    """ВЫдаёт клавиатуру с поэтапной печатью"""
    builder = InlineKeyboardBuilder()
    builder.add(
        InlineKeyboardButton(
            text="Наступне сканирование",
            callback_data=ScanningCallback(
                action=Actions.ACCEPT, task_id=id_, index=index
            ).pack(),
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="Повторное сканирование",
            callback_data=ScanningCallback(
                action=Actions.ACCEPT, task_id=id_, index=index - 1
            ).pack(),
        )
    )
    builder.add(
        InlineKeyboardButton(
            text="Отмена сканирования",
            callback_data=ScanningCallback(
                action=Actions.CANCEL, task_id=id_, index=index
            ).pack(),
        )
    )
    return builder.as_markup()
