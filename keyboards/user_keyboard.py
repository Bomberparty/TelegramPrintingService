from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def get_main_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Создать заказ"), KeyboardButton(text="Помощь")],
        [KeyboardButton(text="Отмена")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                   input_field_placeholder="Выберите способ подачи")
    return keyboard


async def get_task_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Печать"), KeyboardButton(text="Сканирование")],
        [KeyboardButton(text="Отмена"), KeyboardButton(text="Назад")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                   input_field_placeholder="Выберите тип заказа")
    return keyboard


async def get_printing_method_kb() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Одностороння печать"), KeyboardButton(text="Двусторонняя печать")],
        [KeyboardButton(text="Отмена"), KeyboardButton(text="Назад")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


async def pay_way_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="По карте через СБП"), KeyboardButton(text="Наличными при встрече")],
        [KeyboardButton(text="Отмена"), KeyboardButton(text="Назад")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


async def get_simple_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Отмена"), KeyboardButton(text="Назад")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
