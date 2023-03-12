from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def get_main_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Создать заказ"),KeyboardButton(text="Помощь")],
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


async def get_printing_method_kb() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Одностороння печать"), KeyboardButton(text="Двусторонняя печать")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard

async def pay_way_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="По карте через СБП"), KeyboardButton(text="Наличными при встрече")],
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard