from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMStates(StatesGroup):
    delete_list = State()  # состояние "удалить ПС"
    add_list = State()   # состояние "создать ПС"
    add_item = State()  # состояние "создать пункт в ПС"
    del_item = State()  # состояние "удалить пункт в ПС"
    nothing = State()  # ничего не делать???
