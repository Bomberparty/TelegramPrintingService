from aiogram import types
from aiogram.dispatcher.router import Router
from aiogram.filters import Command, Text, or_f, and_f, StateFilter
from aiogram.fsm.context import FSMContext

from keyboards.user_keyboard import *
from states import PrintTask, ChooseTask
from filters import IsAnyAdminsOnShiftFilter


router = Router()


@router.message(and_f(StateFilter("*"),
                      or_f(Text("Отмена"), Command("cancel"))))
async def cancel(message: types.Message, state: FSMContext):
    await state.clear()
    await start(message)


@router.message(or_f(Command("start", "help"),
                     and_f(ChooseTask.step, Text("Назад"))))
async def start(message: types.Message):
    await message.answer('''Доброго времени суток, дорогой пользователь.\n'''
                         '''Для запуска сервиса нажмите\n"Создать заказ" ''',
                         reply_markup=get_main_keyboard())


@router.message(and_f(StateFilter("*"), IsAnyAdminsOnShiftFilter(False)))
async def no_admins(message: types.Message, state: FSMContext):
    await message.answer("Последний админ ушёл, но обещал вернуться =)")
    if state:
        await state.clear()


@router.message(or_f(Text("Создать заказ"),
                     and_f(PrintTask.send_file, Text("Назад"))))
async def create_task(message: types.Message, state: FSMContext):
    await message.answer("Выберите вид заказа",
                         reply_markup=get_choosing_task_keyboard())
    await state.set_state(ChooseTask.step)

