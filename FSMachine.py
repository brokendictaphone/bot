from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

class FSMStates(StatesGroup):
    delete_list = State()  # состояние "удалить ПС"
    add_list = State()   # состояние "создать ПС"