from aiogram import types, F
from aiogram.dispatcher.router import Router
from aiogram.filters import Text, and_f
from aiogram.fsm.context import FSMContext

from keyboards.user_keyboard import *
from keyboards import admin_keyboard
from states import PrintTask, ChooseTask
from loader import bot
from utils.shift import Shift
from utils.utils import prepare_to_downloading, get_number_of_pages
import database


router = Router()


@router.message(PrintTask.number_of_copies, Text("Назад"))
async def require_file(message: types.Message, state: FSMContext):
    await message.answer("Отправьте документ",
                         reply_markup=get_simple_keyboard())
    await state.set_state(PrintTask.send_file)


@router.message(and_f(ChooseTask.step, Text("Печать")))
async def get_task_type(message: types.Message, state: FSMContext):
    id_ = await database.Database().create_new_task(message.from_user.id)
    await state.update_data(task_type=database.TaskType.PRINT_TASK)
    await state.update_data(id=id_)
    await require_file(message, state)


@router.message(PrintTask.choose_printing_mode, Text("Назад"))
async def require_number_of_copies(message: types.Message, state: FSMContext):
    await message.answer("Напишите в чат необходимое вам количество "
                         "копий документа",
                         reply_markup=get_simple_keyboard())
    await state.set_state(PrintTask.number_of_copies)


@router.message(PrintTask.send_file)
async def get_file(message: types.Message, state: FSMContext):
    if message.content_type != types.ContentType.DOCUMENT:
        return await message.answer("Ваше сообщение не содержит документа")
    if message.document.file_name[-4:] != ".pdf":
        return await message.answer("Формат вашего файла отличен от PDF")
    data = await state.get_data()
    file_path = f"media/{data['id']}.pdf"
    prepare_to_downloading(file_path)
    await bot.download(destination=file_path, file=message.document.file_id)

    number_of_pages = get_number_of_pages(file_path)
    if not number_of_pages:
        return await message.answer("Ваш файл не валиден. Я принимю только pdf "
                                    "с форматом A4.")

    await state.update_data(number_of_pages=number_of_pages)
    await state.update_data(file_path=file_path)
    await require_number_of_copies(message, state)


@router.message(PrintTask.choose_pay_way, Text("Назад"))
async def require_printing_mode(message: types.Message, state: FSMContext):
    await message.answer("Выберите режим печати",
                         reply_markup=get_printing_method_kb())
    await state.set_state(PrintTask.choose_printing_mode)


@router.message(PrintTask.number_of_copies, F.text.regexp(r'\d+'))
async def get_copies(message: types.Message, state: FSMContext):
    await state.update_data(number_of_copies=int(message.text))

    await require_printing_mode(message, state)


@router.message(PrintTask.choose_printing_mode)
async def printing_mode(message: types.Message, state: FSMContext):
    if message.text == "Одностороння печать":
        sides_count = database.SidesCount.ONE
    elif message.text == "Двусторонняя печать":
        sides_count = database.SidesCount.TWO
    else:
        return await message.answer("Неккоректный ввод")
    data = await state.get_data()
    await state.update_data(sides_count=sides_count)

    # Необходимо продумать высчитывание стоимости заказа
    coast = data["number_of_pages"] * data["number_of_copies"] * 4
    await state.update_data(coast=coast)
    await message.answer(f'''Стоимость заказа составляет {coast} рублей. 
    Теперь выберите удобный для вас метод оплаты''',
                         reply_markup=pay_way_keyboard())
    await state.set_state(PrintTask.choose_pay_way)


@router.message(PrintTask.choose_pay_way)
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
    task = database.Task(data["id"], message.from_user.id, data["task_type"],
                         data["file_path"], data["number_of_copies"],
                         data["coast"], data["sides_count"], pay_way,
                         database.TaskStatus.CONFIRMING)
    await database.Database().finish_task_creation(task)
    for admin_id in Shift().get_active():
        await bot.send_message(admin_id, f"Новый заказ: {task.id_}",
                               reply_markup=admin_keyboard.get_print_task_keyboard(task.id_))
    await state.clear()
