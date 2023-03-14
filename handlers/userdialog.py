from aiogram import types, F
from aiogram.dispatcher.router import Router
from aiogram.filters import Command, Text, or_f, and_f, StateFilter
from aiogram.fsm.context import FSMContext

from keyboards.user_keyboard import *
from states import CreateTask
from loader import bot

from PyPDF2 import PdfReader

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


@router.message(or_f(and_f(CreateTask.choose_task, Text("Печать")),
                     and_f(CreateTask.number_of_copies, Text("Назад"))))
async def get_task(message: types.Message, state: FSMContext):
    if await state.get_state() == CreateTask.choose_task:
        await state.update_data(service_type="Print")

    await message.answer("Отправьте документ",
                         reply_markup=await get_simple_keyboard())
    await state.set_state(CreateTask.send_file)


@router.message(or_f(CreateTask.send_file,
                     and_f(CreateTask.choose_printing_mode, Text("Назад"))))
async def get_file(message: types.Message, state: FSMContext):
    if await state.get_state() == CreateTask.send_file:
        if message.content_type != types.ContentType.DOCUMENT:
            return await message.answer("Ваше сообщение не содержит документа")
        if message.document.file_name[-4:] != ".pdf":
            return await message.answer("Формат вашего файла отличен от PDF")

        # Будем брать из БД
        task_id = str(message.document.file_id) + str(message.chat.id)
        file_path = f"media/{task_id}.pdf"
        await bot.download(destination=file_path, file=message.document.file_id)
        await state.update_data(file_path=file_path)

    await message.answer("Напишите в чат необходимое вам количество "
                         "копий документа",
                         reply_markup=await get_simple_keyboard())
    await state.set_state(CreateTask.number_of_copies)


@router.message(or_f(and_f(CreateTask.number_of_copies,
                           F.text.regexp(r'\d+')),
                     and_f(CreateTask.choose_pay_way, Text("Назад"))))
async def get_copies(message: types.Message, state: FSMContext):
    if await state.get_state() == CreateTask.number_of_copies:
        await state.update_data(number_of_copies=int(message.text))

    await message.answer("Выберите тип печати",
                         reply_markup=await get_printing_method_kb())
    await state.set_state(CreateTask.choose_printing_mode)


@router.message(CreateTask.choose_printing_mode)
async def printing_mode(message: types.Message, state: FSMContext):
    if message.text == "Одностороння печать":
        double_side = False
    elif message.text == "Двусторонняя печать":
        double_side = True
    else:
        return await message.answer("Неккоректный ввод")
    data = await state.get_data()
    await state.update_data(double_side=double_side)
    number_of_pages = len(PdfReader(data["file_path"]).pages)

    # Необходимо продумать высчитывание стоимости заказа
    task_cost = number_of_pages * data["number_of_copies"] * 4

    await message.answer(f'''Стоимость заказа составляет {task_cost} рублей. 
    Теперь выберите удобный для вас метод оплаты''',
                         reply_markup=await pay_way_keyboard())
    await state.set_state(CreateTask.choose_pay_way)


@router.message(CreateTask.choose_pay_way)
async def pay_way(message: types.Message, state: FSMContext):
    if message.text == "По карте через СБП":
        pass
    elif message.text == "Наличными при встрече":
        await message.answer("Ваш заказ принят к ожиданию. Ожидаем с наличными "
                             "в комнате 254",
                             reply_markup= await get_main_keyboard())
        await state.clear()
