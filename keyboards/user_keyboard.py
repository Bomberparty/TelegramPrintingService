from aiogram.types import ReplyKeyboardMarkup, KeyboardButton,\
    InlineKeyboardButton, InlineKeyboardMarkup


def get_main_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Создать заказ"), KeyboardButton(text="Помощь")],
        [KeyboardButton(text="Отмена")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                   input_field_placeholder="Выберите способ подачи")
    return keyboard


def get_choosing_task_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Печать"), KeyboardButton(text="Сканирование")],
        [KeyboardButton(text="Отмена"), KeyboardButton(text="Назад")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True,
                                   input_field_placeholder="Выберите тип заказа")
    return keyboard


def get_printing_method_kb() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Одностороння печать"), KeyboardButton(text="Двусторонняя печать")],
        [KeyboardButton(text="Отмена"), KeyboardButton(text="Назад")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def pay_way_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="По карте через СБП"), KeyboardButton(text="Наличными при встрече")],
        [KeyboardButton(text="Отмена"), KeyboardButton(text="Назад")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def get_simple_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="Отмена"), KeyboardButton(text="Назад")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard


def get_format_keyboard() -> ReplyKeyboardMarkup:
    kb = [
        [KeyboardButton(text="pdf"), KeyboardButton(text="png")],
        [KeyboardButton(text="Отмена"), KeyboardButton(text="Назад")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    return keyboard
