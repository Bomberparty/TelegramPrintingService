from aiogram.dispatcher.router import Router
from aiogram.filters import or_f, and_f
from aiogram.types import CallbackQuery
from aiogram import F

from keyboards.callbacks import AdminPrintTaskCallback, Actions, \
    PrintTaskCompletingCallback, AdminScanTaskCallback
from keyboards.admin_keyboard import get_print_completing_task_keyboard
from database import TaskDB, TaskStatus
from loader import bot
from utils.shift import Shift
from filters import AdminPrintTaskStatusFilter, TaskCompletingStatusFilter
from utils.print import print_file, PrintException

import logging

router = Router()


@router.callback_query(and_f(AdminPrintTaskCallback.filter(F.action == Actions.ACCEPT),
                             AdminPrintTaskStatusFilter(TaskStatus.CONFIRMING)))
async def accept_task(callback: CallbackQuery,
                      callback_data: AdminPrintTaskCallback):
    task = await TaskDB().get_task(callback_data.task_id)
    try:
        await callback.message.edit_text(f"Началась печать заказа № {task.id_}",
                                         reply_markup=get_print_completing_task_keyboard(task.id_))
        await bot.send_message(task.user_id, "Началась печать")
        await print_file(file_path=task.file_path, copies=task.number_of_copies,
                         mode=task.sides_count)
        await TaskDB().update_task_status(task.id_, TaskStatus.PENDING)
    except PrintException as ex:
        logging.exception(ex)
        await callback.message.edit_text(f"Печать заказа № {task.id_}"
                                         f" провалилась")
        await bot.send_message(task.user_id, "Печать провалилась")
        await TaskDB().update_task_status(task.id_, TaskStatus.FAILED)
    except Exception as ex:
        logging.exception(ex)


@router.callback_query(
    and_f(PrintTaskCompletingCallback.filter(F.action == Actions.ACCEPT),
          TaskCompletingStatusFilter(TaskStatus.PENDING)))
async def task_complete(callback: CallbackQuery,
                        callback_data: PrintTaskCompletingCallback):
    task = await TaskDB().get_task(callback_data.task_id)
    await TaskDB().update_task_status(task.id_, TaskStatus.FINISHED)
    await callback.message.edit_text(f"Печать заказа № {task.id_} завершилась")
    await bot.send_message(task.user_id, "Печать завершилась")


@router.callback_query(
    and_f(PrintTaskCompletingCallback.filter(F.action == Actions.CANCEL),
          TaskCompletingStatusFilter(TaskStatus.PENDING)))
async def task_failed(callback: CallbackQuery,
                      callback_data: PrintTaskCompletingCallback):
    task = await TaskDB().get_task(callback_data.task_id)
    await TaskDB().update_task_status(task.id_, TaskStatus.FAILED)
    await callback.message.edit_text("Печать провалилась")
    await bot.send_message(task.user_id, "Печать успешно провалилась. Свяжитесь"
                                         " с админами из 254 комнаты")


@router.callback_query(PrintTaskCompletingCallback.filter())
@router.callback_query(AdminPrintTaskCallback.filter())
@router.callback_query(AdminScanTaskCallback.filter())
async def bad_task(callback: CallbackQuery):
    await callback.message.edit_text("Заказ уже завершён, отменён или выполнен")
