from aiogram.dispatcher.router import Router
from aiogram.filters import or_f, and_f
from aiogram.types import CallbackQuery
from aiogram import F, types

from keyboards.callbacks import AdminPrintTaskCallback, Actions, \
    PrintTaskCompletingCallback, AdminScanTaskCallback, ScanningCallback
from keyboards.admin_keyboard import get_scanning_keyboard
from database import Database, TaskStatus
from loader import bot
from utils.shift import Shift
from filters import AdminScanTaskStatusFilter
from utils.scan import scan_file

import logging


router = Router()


@router.callback_query(and_f(AdminScanTaskCallback.filter(F.action == Actions.ACCEPT),
                             AdminScanTaskStatusFilter(TaskStatus.CONFIRMING)))
async def accept_task(callback: CallbackQuery,
                      callback_data: AdminScanTaskCallback):
    task = await Database().get_task(callback_data.task_id)
    await callback.message.edit_text(f"Сканирование заказа № {task.id_} \n"
                                     f"Страница №1/{task.number_of_copies}",
                                     reply_markup=get_scanning_keyboard(task.id_
                                                                        , 1))
    await bot.send_message(task.user_id, "Скоро админ начнёт сканирование")

    await Database().update_task_status(task.id_, TaskStatus.PENDING)


@router.callback_query(ScanningCallback.filter(F.action == Actions.ACCEPT))
async def scan_page(callback: CallbackQuery, callback_data: ScanningCallback):
    task = await Database().get_task(callback_data.task_id)
    file_path = await scan_file(task.id_, callback_data.index, task.format)
    await bot.send_message(task.user_id, f"Страница №{callback_data.index}")
    await bot.send_document(task.user_id, types.FSInputFile(file_path))
    if task.number_of_copies == callback_data.index:
        await bot.send_message(task.user_id, f"Сканированик №{task.id_} завершилось. "
                               f"Приходите ещё")
        await callback.message.edit_text(f"Сканирование заказа №{task.id_} "
                                         f"завершилось.", reply_markup=None)
        return

    await callback.message.edit_text(f"Сканирование заказа №{task.id_} \n"
                                     f"страница №{callback_data.index}/"
                                     f"{task.number_of_copies}",
                                     reply_markup=get_scanning_keyboard(task.id_, callback_data.index + 1))
