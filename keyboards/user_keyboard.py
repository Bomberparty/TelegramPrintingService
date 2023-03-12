from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def get_main_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Создать заказ"), KeyboardButton(text="Помощь"), KeyboardButton(text="Связь с админами")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                   input_field_placeholder="Выберите способ подачи")
    return keyboard


async def get_task_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Печать"), KeyboardButton(text="Сканирование")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                   input_field_placeholder="Выберите тип заказа")
    return keyboard
