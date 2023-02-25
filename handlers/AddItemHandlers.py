from keyboard import kb_start, manage_list_kbrd
from aiogram.dispatcher import FSMContext
from FSMachine import FSMStates
from aiogram import types, Dispatcher
from funct import del_mess, msg_id_write, view_list
import sqlite3 as sq


async def add_item(message: types.Message, state: FSMContext):
    id = message.chat.id
    data_base = sq.connect('ListBotBase2.db')
    cur = data_base.cursor()
    list_name = cur.execute(f"SELECT list_name FROM current_list WHERE user_id = {id} ").fetchone()[0]  # определение ПС
    await del_mess(id)  # удаление предыдущего сообщения
    data_base = sq.connect('ListBotBase2.db')
    cur = data_base.cursor()
    if message.text == 'выход из списка':
        msg = await message.answer(f'Что нужно сделать?', reply_markup=kb_start)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await state.finish()  # выключение машины состояний
        await message.delete()  # удалить сообщение пользователя
    elif message.text == 'удалить из списка':
        await state.finish()  # выключение машины состояний
        await message.delete()  # удалить сообщение пользователя
        list_kb = view_list(id, list_name)
        msg = await message.answer(f'Какой пункт нужно удалить?', reply_markup=list_kb)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await FSMStates.del_item.set()  # включение состояния "удалить пункт в ПС"
    elif '"' in message.text:
        msg = await message.answer('Нельзя использовать кавычки! Введи без них')
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя
    elif len(message.text) > 25:
        msg = await message.answer('Слишком длинно, не возьмусь')
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя
    else:
        cur.execute("""INSERT INTO lists VALUES(?,?,?)""",
                    (id, list_name, message.text))  # добавление данных в список дел
        data_base.commit()  # подтверждение действий
        await del_mess(id)  # удаление предыдущего сообщения
        list_kb = view_list(id, list_name)  # функция создает пункты пользовательских списков в виде клавиатуры
        msg = await message.answer(f'Вот и добавили "{message.text}" в список. Добавим ещё что-то?', reply_markup=list_kb)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        msg2 = await message.answer(f'Что ещё нужно добавить в список?', reply_markup=manage_list_kbrd)
        msg_id_write(msg2, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя


def register_add_item_handlers(dp: Dispatcher):
    dp.register_message_handler(add_item, state=FSMStates.add_item)  # добавление пунктов в пользовательский список
    dp.register_message_handler(add_item, state=FSMStates.del_item)  # добавление пунктов в пользовательский список
