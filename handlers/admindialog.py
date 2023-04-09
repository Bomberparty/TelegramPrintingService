from aiogram.dispatcher.router import Router
from aiogram.filters import Command, Text, or_f, and_f, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram import F

from keyboards.callbacks import AdminTaskCallback, Actions, \
    TaskCompletingCallback
from keyboards.admin_keyboard import get_completing_task_keyboard
from database import Database, TaskStatus
from loader import bot
from utils.shift import Shift
from filters import AdminTaskStatusFilter, IsAdminFilter,\
    TaskCompletingStatusFilter
from utils.print import print_file, PrintException

import logging

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


@router.callback_query(and_f(AdminTaskCallback.filter(F.action == Actions.CANCEL),
                             AdminTaskStatusFilter(TaskStatus.CONFIRMING)))
async def cancel_task(callback: CallbackQuery,
                      callback_data: AdminTaskCallback):
    db = Database()
    message = f"Заказ №{callback_data.task_id} отменён."
    await db.update_task_status(callback_data.task_id, TaskStatus.CANCELED)
    await callback.message.edit_text(message)
    user_id = await db.get_user_id_by_task_id(callback_data.task_id)
    for admin_id in Shift.get_active():
        if admin_id != callback.from_user.id:
            await bot.send_message(admin_id, message)
    await bot.send_message(user_id, f"Ваш заказ был отменён злым админом.")


@router.callback_query(and_f(AdminTaskCallback.filter(F.action == Actions.ACCEPT),
                             AdminTaskStatusFilter(TaskStatus.CONFIRMING)))
async def accept_task(callback: CallbackQuery,
                      callback_data: AdminTaskCallback):
    task = await Database().get_task(callback_data.task_id)
    try:
        await callback.message.edit_text(f"Началась печать заказа № {task.id_}",
                                         reply_markup= await get_completing_task_keyboard(task.id_))
        await bot.send_message(task.user_id, "Началась печать")
        await print_file(file_path=task.file_path, copies=task.number_of_copies,
                         mode=task.sides_count)
        await Database().update_task_status(task.id_, TaskStatus.PENDING)
    except PrintException as ex:
        logging.exception(ex)
        await callback.message.edit_text(f"Печать заказа № {task.id_}"
                                         f" провалилась")
        await bot.send_message(task.user_id, "Печать провалилась")
        await Database().update_task_status(task.id_, TaskStatus.FAILED)
    except Exception as ex:
        logging.exception(ex)


@router.callback_query(
    and_f(TaskCompletingCallback.filter(F.action == Actions.ACCEPT),
          TaskCompletingStatusFilter(TaskStatus.PENDING)))
async def task_complete(callback: CallbackQuery,
                        callback_data: TaskCompletingCallback):
    task = await Database().get_task(callback_data.task_id)
    await Database().update_task_status(task.id_, TaskStatus.FINISHED)
    await callback.message.edit_text(f"Печать заказа № {task.id_} завершилась")
    await bot.send_message(task.user_id, "Печать завершилась")


@router.callback_query(
    and_f(TaskCompletingCallback.filter(F.action == Actions.CANCEL),
          TaskCompletingStatusFilter(TaskStatus.PENDING)))
async def task_failed(callback: CallbackQuery,
                      callback_data: TaskCompletingCallback):
    task = await Database().get_task(callback_data.task_id)
    await Database().update_task_status(task.id_, TaskStatus.FAILED)
    await callback.message.edit_text("Печать провалилась")
    await bot.send_message(task.user_id, "Печать успешно провалилась. Свяжитесь"
                                         " с админами из 254 комнаты")


@router.callback_query(or_f(TaskCompletingCallback, AdminTaskStatusFilter))
async def bad_task(callback: CallbackQuery):
    await callback.message.edit_text("Заказ уже завершён, отменён или выполнен")
