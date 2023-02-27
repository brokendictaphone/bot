from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from FSMachine import FSMStates
from keyboard import kb_start
from funct import *
import sqlite3 as sq


async def add_list_button(message: types.Message):  # кнопка создать список
    id = message.chat.id
    await del_mess(id)  # удаление предыдущего сообщения
    list_len = check_lists_numb(id)  # проверка количества польовательских списков
    if list_len < 3:
        msg = await message.answer('Введите название нового списка: ')
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя
        await FSMStates.add_list.set()  # включено состояние "создать ПС"
    else:
        msg = await message.answer('Нельзя создать больше 3 списков!', reply_markup=kb_start)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя


async def add_list(message: types.Message, state: FSMContext):  # создание ПС
    id = message.chat.id
    await del_mess(id)  # удаление предыдущего сообщения
    data_base = sq.connect('ListBotBase2.db')
    cur = data_base.cursor()
    cur.execute("""INSERT INTO lists VALUES(?,?,?)""", (id, message.text, None))  # добавление нового списка
    data_base.commit()  # подтверждение действий
    data_base.close()
    current_list_write(message.text, id)  # запись текущего списка в БД
    msg = await message.answer(f'Вот и создан список "{message.text}".'
                               f' Напишите, что нужно добавить в него?', reply_markup=kb_start)
    msg_id_write(msg, id)  # записывает айди сообщения в БД
    await message.delete()  # удалить сообщение пользователя
    await state.finish()  # выключение машины состояний
    await FSMStates.add_item.set()  # состояние "создать пункт в ПС"


async def prompt_mess(message: types.Message):  # подсказка
    id = message.chat.id
    await del_mess(id)  # удаление предыдущего сообщения
    msg = await message.answer(f'Сначала нужно нажать кнопку "создать список"!', reply_markup=kb_start)
    msg_id_write(msg, id)  # записывает айди сообщения в БД
    await message.delete()  # удалить сообщение пользователя


def register_AddLIst_handlers(dp: Dispatcher):
    dp.register_message_handler(add_list_button, (Text(equals='создать список')), state=None)  # кнопка "создать список"
    dp.register_message_handler(add_list, state=FSMStates.add_list)  # создание списка
    dp.register_message_handler(prompt_mess, state=None)  # подсказка



