from aiogram.dispatcher.router import Router
from aiogram.filters import Command, Text, or_f, and_f, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram import F

from keyboards.callbacks import AdminTaskCallback, Actions
from database import Database, TaskStatus
from loader import admins, bot
from filters import IsNotConfirmingFilter, IsAdminFilter
from utils.print import print_file, PrintException

import logging


router = Router()


@router.callback_query(IsNotConfirmingFilter())
async def bad_task(callback: CallbackQuery):
    await callback.message.edit_text("Заказ уже завершён, отменён или выполнен")


@router.callback_query(AdminTaskCallback.filter(F.action == Actions.CANCEL))
async def cancel_task(callback: CallbackQuery,
                      callback_data: AdminTaskCallback):
    db = Database()
    message = f"Заказ №{callback_data.task_id} отменён."
    await db.update_task_status(callback_data.task_id, TaskStatus.CANCELED)
    await callback.message.edit_text(message)
    user_id = await db.get_user_id_by_task_id(callback_data.task_id)
    for admin_id in admins:
        if admin_id != callback.from_user.id:
            await bot.send_message(admin_id, message)
    await bot.send_message(user_id, f"Ваш заказ был отменён злым админом.")


@router.callback_query(AdminTaskCallback.filter(F.action == Actions.ACCEPT))
async def accept_task(callback: CallbackQuery,
                      callback_data: AdminTaskCallback):
    task = await Database().get_task(callback_data.task_id)
    try:
        await callback.message.edit_text("Началась печать")
        await bot.send_message(task.user_id, "Началась печать")
        await print_file(file_path=task.file_path, copies=task.number_of_copies,
                         mode=task.sides_count)
    except PrintException as ex:
        logging.exception(ex)
        await Database().update_task_status(task.id_, TaskStatus.PENDING)
        await callback.message.edit_text("Печать провалилась")
        await bot.send_message(task.user_id, "Печать провалилась")
        for admin_id in admins:
            await bot.send_message(admin_id, f"Печать заказа № {task.id_} "
                                             f"провалилась. Стоимость: "
                                             f"{task.coast}")
        await Database().update_task_status(task.id_, TaskStatus.FAILED)
        return
    except Exception as ex:
        logging.exception(ex)
        return

    await Database().update_task_status(task.id_, TaskStatus.FINISHED)
    await callback.message.edit_text("Печать завершилась")
    await bot.send_message(task.user_id, "Печать завершилась")
    for admin_id in admins:
        await bot.send_message(admin_id, f"Печать заказа № {task.id_} "
                                         f"Успешно завершилась. Стоимость: "
                                         f"{task.coast}")
