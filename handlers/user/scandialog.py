from aiogram import types, F
from aiogram.dispatcher.router import Router
from aiogram.filters import Text, and_f, or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

import database
from keyboards import admin_keyboard
from keyboards.callbacks import CardCallback, Actions
from keyboards.user_keyboard import get_simple_keyboard, get_format_keyboard, \
    pay_way_keyboard, get_main_keyboard, get_card_keyboard
from loader import bot
from states import ChooseTask, ScanTask
from utils import payment
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
                         reply_markup=pay_way_keyboard(coast))
    await state.set_state(ScanTask.choose_pay_way)


@router.message(ScanTask.choose_pay_way, Text("По карте через СБП"))
async def pay_online(message: types.Message, state: FSMContext):
    numbers = Shift().get_active_number()
    msg = 'Переведите средства через СБП в банк "Тинькофф" по номер'+ \
          ('у: ' if len(numbers) == 1 else 'ам: ')
    for index in range(len(numbers)):
        msg += ("+7"+str(numbers[index]) +
                (" или " if index != len(numbers) - 1 else ""))
    await message.answer(msg, reply_markup=get_main_keyboard())
    task = await finish_creation(message, state, database.PayWay.ONLINE)
    await print_task_information_to_admins(task)


@router.message(ScanTask.choose_pay_way, Text("Наличными при встрече"))
async def pay_cash(message: types.Message, state: FSMContext):
    await message.answer("Ваш заказ принят к ожиданию. Ожидаем с наличными "
                         "в комнате 254.",
                         reply_markup=get_main_keyboard())
    task = await finish_creation(message, state, database.PayWay.CASH)
    await print_task_information_to_admins(task)


@router.message(ScanTask.choose_pay_way, Text("По карте на Юмани"))
async def pay_card(message: types.Message, state: FSMContext):
    task = await finish_creation(message, state, database.PayWay.CARD)
    id_ = await database.TransactionDB().create_transaction(task.id_,
                                                            task.user_id)
    url = payment.create_pay_link(id_, task.coast)
    await message.answer(f"Для начала сканирования оплатите по ссылке {url}",
                         reply_markup=get_card_keyboard(id_, database.TaskType.SCAN_TASK, task.id_))
    await message.answer(text="После оплаты нажмите на кнопку 'проверить'",
                         reply_markup=get_main_keyboard())


async def finish_creation(message: types.Message, state: FSMContext,
                          pay_way: database.PayWay) -> database.Task:
    data = await state.get_data()
    task = database.Task(id_=data["id"], user_id=message.from_user.id,
                         task_type=data["task_type"], file_path=None,
                         number_of_copies=data["number_of_copies"],
                         coast=data["coast"], sides_count=None,
                         format=data["format"], pay_way=pay_way,
                         status=database.TaskStatus.CONFIRMING)
    await database.TaskDB().finish_scan_task_creation(task)
    await state.clear()
    return task


async def print_task_information_to_admins(task: database.Task):
    for admin_id in Shift().get_active():
        await bot.send_message(admin_id, f"Новый заказ сканирования №: {task.id_}."
                                         f" Его стоимость составляет {task.coast} рублей.",
                               reply_markup=admin_keyboard.get_scan_task_keyboard(task.id_))


@router.callback_query(and_f(CardCallback.filter(F.action == Actions.ACCEPT),
                             CardCallback.filter(F.task_type == database.TaskType.SCAN_TASK)))
async def check_transaction(callback: CallbackQuery, callback_data: CardCallback):
    for admin_id in Shift().get_active():
        await bot.send_message(admin_id, f"СРОЧНО!. Оплачен заказ №: {callback_data.id_}.",
                               reply_markup=admin_keyboard.get_scan_task_keyboard(callback_data.task_id))