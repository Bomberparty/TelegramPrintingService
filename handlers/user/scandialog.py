from aiogram import types, F
from aiogram.dispatcher.router import Router
from aiogram.filters import Text, and_f, or_f
from aiogram.fsm.context import FSMContext

import database
from keyboards import admin_keyboard
from keyboards.user_keyboard import get_simple_keyboard, get_format_keyboard, \
    pay_way_keyboard, get_main_keyboard
from loader import bot
from states import ChooseTask, ScanTask
from utils.shift import Shift

router = Router()


@router.message(ScanTask.choose_format, Text("Назад"))
async def require_number_of_documents(message: types.Message, state: FSMContext):
    await message.answer("Напишите в чат необходимое вам количество "
                         "копий документа",
                         reply_markup=get_simple_keyboard())
    await state.set_state(ScanTask.number_of_documents)


@router.message(and_f(ChooseTask.step, Text("Сканирование")))
async def get_task_type(message: types.Message, state: FSMContext):
    id_ = await database.TaskDB().create_new_task(message.from_user.id)
    await state.update_data(task_type=database.TaskType.SCAN_TASK)
    await state.update_data(id=id_)
    await require_number_of_documents(message, state)


@router.message(and_f(ScanTask.choose_pay_way, Text("Назад")))
async def require_format(message: types.Message, state: FSMContext):
    await message.answer("Выберите формат изображения",
                         reply_markup=get_format_keyboard())
    await state.set_state(ScanTask.choose_format)


@router.message(and_f(ScanTask.number_of_documents, F.text.regexp(r'\d+')))
async def get_number_of_documents(message: types.Message, state: FSMContext):
    await state.update_data(number_of_copies=int(message.text))
    await require_format(message, state)


@router.message(and_f(ScanTask.choose_format, or_f(Text("pdf"), Text("png"))))
async def get_format(message: types.Message, state: FSMContext):
    await state.update_data(format=message.text)
    data = await state.get_data()

    coast = data["number_of_copies"] * 4
    await state.update_data(coast=coast)
    await message.answer(f'''Стоимость заказа составляет {coast} рублей. 
    Теперь выберите удобный для вас метод оплаты''',
                         reply_markup=pay_way_keyboard())
    await state.set_state(ScanTask.choose_pay_way)


@router.message(ScanTask.choose_pay_way)
async def pay_way(message: types.Message, state: FSMContext):
    if message.text == "По карте через СБП":
        pay_way = database.PayWay.CARD
        numbers = Shift().get_active_number()
        msg = 'Переведите средства через СБП в банк "Тинькофф" по номер'+ \
              ('у: ' if len(numbers) == 1 else 'ам: ')
        for index in range(len(numbers)):
            msg += ("+7"+str(numbers[index]) +
                    (" или " if index != len(numbers) - 1 else ""))
        await message.answer(msg, reply_markup=get_main_keyboard())

    elif message.text == "Наличными при встрече":
        pay_way = database.PayWay.CASH
        await message.answer("Ваш заказ принят к ожиданию. Ожидаем с наличными "
                             "в комнате 254.",
                             reply_markup=get_main_keyboard())
    else:
        return
    data = await state.get_data()
    task = database.Task(id_=data["id"], user_id=message.from_user.id, task_type=data["task_type"],
                         file_path=None, number_of_copies=data["number_of_copies"],
                         coast=data["coast"], sides_count=None,
                         format=data["format"], pay_way=pay_way,
                         status=database.TaskStatus.CONFIRMING)
    await database.TaskDB().finish_scan_task_creation(task)
    for admin_id in Shift().get_active():
        await bot.send_message(admin_id, f"Новый заказ печати №: {task.id_}",
                               reply_markup=admin_keyboard.get_scan_task_keyboard(task.id_))
    await state.clear()
