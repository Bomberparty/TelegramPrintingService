from aiogram import types, F
from aiogram.dispatcher.router import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext

from keyboards.user_keyboard import get_main_keyboard, get_task_keyboard
from states import CreateTask
from loader import bot

router = Router()


@router.message(Command("start", "help"))
async def start(message: types.Message):
    await message.answer("Шевцов - ВЕЛИКИЙ чоловiк", reply_markup=await get_main_keyboard())


@router.message(Text("Создать заказ"))
async def create_task(message: types.Message, state: FSMContext):
    await message.answer("Выберите вид заказа", reply_markup=await get_task_keyboard())
    await state.set_state(CreateTask.choose_task)


@router.message(CreateTask.choose_task, Text("Печать"))
async def get_task(message: types.Message, state: FSMContext):
    await state.update_data(service_type="Print")
    await message.answer("Отправьте документ")


@router.message(CreateTask.send_file)
async def get_file(message: types.Message, state: FSMContext):
    print(message.content_type, type(message.content_type))
    if message.content_type != types.ContentType.DOCUMENT:
        return await message.answer("Ваше сообщение не содержит документа")
    if message.document.file_name[-4:] != ".pdf":
        return await message.answer("Формат вашего файла отличен от PDF")

    # Будем брать из БД
    task_id = str(message.from_user.id) + str(message.chat.id)
    file_path = f"media/{task_id}.pdf"
    await bot.download(destination=file_path, file=message.document.file_id)

    await state.update_data(file_path=file_path)
    await state.set_state(CreateTask.send_repetition)
