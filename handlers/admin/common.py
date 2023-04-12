from aiogram.dispatcher.router import Router
from aiogram.filters import Command, and_f
from aiogram.types import Message

from keyboards.admin_keyboard import get_task_keyboard
from database import Database
from utils.shift import Shift
from filters import IsAdminFilter

router = Router()


@router.message(and_f(Command("start_shift"), IsAdminFilter(True)))
async def start_shift(message: Message):
    if Shift.start(message.from_user.id):
        return await message.answer("Вы вышли на смену")
    await message.answer("Ты идиот?")


@router.message(and_f(Command("end_shift"), IsAdminFilter(True)))
async def finish_shift(message: Message):
    if Shift.end(message.from_user.id):
        return await message.answer("Вы успешно ушли со смены. Хорошего отдыха")
    await message.answer("Дармоед, ты и так уже не работаешь.")


@router.message(and_f(Command("gctl"), IsAdminFilter(True)))
async def get_confirming_task_list(message: Message):
    tasks = await Database().get_confirming_task_list()
    await message.answer("Список действующих заказов:")
    for id_ in tasks:
        kb = get_task_keyboard(id_[0])
        await message.answer(f"Заказ №{id_[0]}", reply_markup=kb)