from aiogram.fsm.state import StatesGroup, State


class ChooseTask(StatesGroup):
    step = State()


class PrintTask(StatesGroup):
    send_file = State()
    number_of_copies = State()
    choose_printing_mode = State()
    choose_pay_way = State()


class ScanTask(StatesGroup):
    number_of_documents = State()
    choose_format = State()
    choose_pay_way = State()

