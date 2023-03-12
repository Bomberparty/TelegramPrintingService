from aiogram.fsm.state import StatesGroup, State


class CreateTask(StatesGroup):
    choose_task = State()
    send_file = State()
    send_repetition = State()
    choose_printing_mode = State()
    choose_pay_way = State()

