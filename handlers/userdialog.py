from PyPDF2.errors import PdfReadError
from aiogram import types, F
from aiogram.dispatcher.router import Router
from aiogram.filters import Command, Text, or_f, and_f, StateFilter
from aiogram.fsm.context import FSMContext
from PyPDF2 import PdfReader

from keyboards.user_keyboard import *
from states import CreateTask
from loader import bot
from utils.utils import prepare_to_downloading
import database


router = Router()


@router.message(and_f(StateFilter("*"),
                      or_f(Text("Отмена"), Command("cancel"))))
async def cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await start(message)


@router.message(or_f(Command("start", "help"),
                     and_f(CreateTask.choose_task, Text("Назад"))))
async def start(message: types.Message):
    await message.answer('''Доброго времени суток, дорогой пользователь.\n'''
                         '''Для запуска сервиса нажмите\n"Создать заказ" ''',
                         reply_markup=await get_main_keyboard())


@router.message(or_f(Text("Создать заказ"),
                     and_f(CreateTask.send_file, Text("Назад"))))
async def create_task(message: types.Message, state: FSMContext):
    await message.answer("Выберите вид заказа",
                         reply_markup=await get_task_keyboard())
    await state.set_state(CreateTask.choose_task)


@router.message(CreateTask.number_of_copies, Text("Назад"))
async def require_file(message: types.Message, state: FSMContext):
    await message.answer("Отправьте документ",
                         reply_markup=await get_simple_keyboard())
    await state.set_state(CreateTask.send_file)


@router.message(and_f(CreateTask.choose_task, Text("Печать")))
async def get_task_type(message: types.Message, state: FSMContext):
    id_ = await database.Database().create_new_task(message.from_user.id)
    await state.update_data(task_type=database.TaskType.PRINT_TASK)
    await state.update_data(id=id_)
    await require_file(message, state)


@router.message(CreateTask.choose_printing_mode, Text("Назад"))
async def require_number_of_copies(message: types.Message, state: FSMContext):
    await message.answer("Напишите в чат необходимое вам количество "
                         "копий документа",
                         reply_markup=await get_simple_keyboard())
    await state.set_state(CreateTask.number_of_copies)


@router.message(CreateTask.send_file)
async def get_file(message: types.Message, state: FSMContext):
    if message.content_type != types.ContentType.DOCUMENT:
        return await message.answer("Ваше сообщение не содержит документа")
    if message.document.file_name[-4:] != ".pdf":
        return await message.answer("Формат вашего файла отличен от PDF")
    data = await state.get_data()
    file_path = f"media/{data['id']}.pdf"
    prepare_to_downloading(file_path)
    await bot.download(destination=file_path, file=message.document.file_id)

    try:
        number_of_pages = len(PdfReader(file_path).pages)
    except PdfReadError:
        return await message.answer("PDF файл не валиден")

    await state.update_data(number_of_pages=number_of_pages)
    await state.update_data(file_path=file_path)
    await require_number_of_copies(message, state)


@router.message(CreateTask.choose_pay_way, Text("Назад"))
async def require_printing_mode(message: types.Message, state: FSMContext):
    await message.answer("Выберите режим печати",
                         reply_markup=await get_printing_method_kb())
    await state.set_state(CreateTask.choose_printing_mode)


@router.message(CreateTask.number_of_copies, F.text.regexp(r'\d+'))
async def get_copies(message: types.Message, state: FSMContext):
    await state.update_data(number_of_copies=int(message.text))

    await require_printing_mode(message, state)


@router.message(CreateTask.choose_printing_mode)
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
                         reply_markup=await pay_way_keyboard())
    await state.set_state(CreateTask.choose_pay_way)


@router.message(CreateTask.choose_pay_way)
async def pay_way(message: types.Message, state: FSMContext):
    if message.text == "По карте через СБП":
        pay_way = database.PayWay.CARD
    elif message.text == "Наличными при встрече":
        pay_way = database.PayWay.CASH
        await message.answer("Ваш заказ принят к ожиданию. Ожидаем с наличными "
                             "в комнате 254",
                             reply_markup=await get_main_keyboard())
    else:
        return
    data = await state.get_data()
    task = database.Task(data["id"], message.from_user.id, data["task_type"],
                         data["file_path"], data["number_of_copies"],
                         data["coast"], data["sides_count"], pay_way,
                         database.TaskStatus.CONFIRMING)
    await database.Database().finish_task_creation(task)
    await state.clear()
