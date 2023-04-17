from aiogram import F
from aiogram.dispatcher.router import Router
from aiogram.filters import Command, and_f
from aiogram.types import Message, CallbackQuery

from keyboards.admin_keyboard import get_print_task_keyboard, \
    get_scan_task_keyboard
from database import Database, TaskStatus, TaskType
from keyboards.callbacks import AdminPrintTaskCallback, Actions, \
    AdminScanTaskCallback
from loader import bot
from utils.shift import Shift
from filters import IsAdminFilter, AdminPrintTaskStatusFilter, \
    AdminScanTaskStatusFilter

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


@router.message(and_f(Command("gcptl"), IsAdminFilter(True)))
async def get_confirming_task_list(message: Message):
    tasks = await Database().get_confirming_task_list(TaskType.PRINT_TASK)
    await message.answer("Список действующих заказов на печать:")
    for id_ in tasks:
        kb = get_print_task_keyboard(id_[0])
        await message.answer(f"Заказ №{id_[0]}", reply_markup=kb)


@router.message(and_f(Command("gcstl"), IsAdminFilter(True)))
async def get_confirming_task_list(message: Message):
    tasks = await Database().get_confirming_task_list(TaskType.SCAN_TASK)
    await message.answer("Список действующих заказов на сканирование:")
    for id_ in tasks:
        kb = get_scan_task_keyboard(id_[0])
        await message.answer(f"Заказ №{id_[0]}", reply_markup=kb)


@router.callback_query(and_f(AdminPrintTaskCallback.filter(F.action == Actions.CANCEL),
                             AdminPrintTaskStatusFilter(TaskStatus.CONFIRMING)))
@router.callback_query(and_f(AdminScanTaskCallback.filter(F.action == Actions.CANCEL),
                             AdminScanTaskStatusFilter(TaskStatus.CONFIRMING)))
async def cancel_task(callback: CallbackQuery,
                      callback_data: AdminPrintTaskCallback):
    db = Database()
    message = f"Заказ №{callback_data.task_id} отменён."
    await db.update_task_status(callback_data.task_id, TaskStatus.CANCELED)
    await callback.message.edit_text(message)
    user_id = await db.get_user_id_by_task_id(callback_data.task_id)
    for admin_id in Shift.get_active():
        if admin_id != callback.from_user.id:
            await bot.send_message(admin_id, message)
    await bot.send_message(user_id, f"Ваш заказ был отменён злым админом.")