from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from keyboard import kb_start
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from funct import *
import sqlite3 as sq

def AddFlag_write(AddFlag, id):
    """записывает AddFlag в БД"""
    data_base = sq.connect('ListBotBase2.db')  # добавление данных в список дел
    cur = data_base.cursor()
    cur.execute(f"SELECT AddFlag FROM flags WHERE user_id = {id} ")  # выбор значения
    if cur.fetchone():
        cur.execute(f'UPDATE flags SET AddFlag = {AddFlag} WHERE user_id = {id}')
    else:
        cur.execute("""INSERT INTO flags(user_id,AddFlag) VALUES(?,?)""",
                    (id, AddFlag))  # добавление данных
    data_base.commit()  # подтверждение действий
    data_base.close()  # закрытие ДБ


def view_user_lists(id):
    """создает и возвращет пользовательские списки в виде клавиатуры"""
    list_kb = InlineKeyboardMarkup()  # создание клавиатуры списка
    data_base = sq.connect('ListBotBase2.db')  # связь с БД
    cur = data_base.cursor()
    for list in cur.execute(f"SELECT list FROM lists WHERE user_id = {id}"):  # вывод данных из БД(выбрать всё из таблицы пользователи)
        for tpl in list:
            b = InlineKeyboardButton(tpl, callback_data=tpl)
            list_kb.row(b)
    return list_kb


def check_lists_numb(id):
    """проверка количества списков"""
    data_base = sq.connect('ListBotBase2.db')  # связь с БД
    cur = data_base.cursor()
    res = cur.execute(f"SELECT list FROM lists WHERE user_id = {id}") # вывод данных из БД(выбрать всё из таблицы пользователи)
    length = len(res.fetchall())
    return length

async def add_list(message: types.Message):  # создание списка
    id = message.chat.id
    list_len = check_lists_numb(id)
    if list_len < 3:
        await message.answer('Введите название нового списка: ')
        AddFlag = 1
        AddFlag_write(AddFlag, id)  # запись AddFlag в БД
    else:
        await message.answer('Нельзя создать больше 3 списков!',reply_markup=kb_start)
        AddFlag = 0
        AddFlag_write(AddFlag, id)  # запись AddFlag в БД


async def insert_list(message: types.Message):
    id = message.chat.id
    await del_mess(id)  # удаление предыдущего сообщения
    data_base = sq.connect('ListBotBase2.db')
    cur = data_base.cursor()
    AddFlag = cur.execute(f"SELECT AddFlag FROM flags WHERE user_id = {id}").fetchone()[0]
    if AddFlag == 1:
        cur.execute("""INSERT INTO lists VALUES(?,?,?)""", (id, message.text, None))  # добавление нового списка
        data_base.commit()  # подтверждение действий
        msg = await message.answer(f'Вот и создан список "{message.text}"', reply_markup=kb_start)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя
        AddFlag = 0
        AddFlag_write(AddFlag, id)  # запись AddFlag в БД
    else:
        if message.text == 'показать списки':
            pass
        else:
            msg = await message.answer(f'Сначала нужно нажать кнопку "создать список"!', reply_markup=kb_start)
            msg_id_write(msg, id)  # записывает айди сообщения в БД
            await message.delete()  # удалить сообщение пользователя


async def add_lists_button(message: types.Message):
    id = message.chat.id
    await del_mess(id)  # удаление предыдущего сообщения
    flag = check_data_base(id)
    if flag:
        list_kb = view_user_lists(id)  # функция создает и возвращет списки пользователя в виде клавиатуры
        msg = await message.answer('Актуальные списки: ', reply_markup=list_kb)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя
    else:
        msg = await message.answer('Нечего показать-то! Ни одного списка не создано...', reply_markup=kb_start)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя


def register_AddLIst_handlers(dp: Dispatcher):
    dp.register_message_handler(add_list, (Text(equals='создать список')))  # создание списка
    dp.register_message_handler(add_lists_button, (Text(equals='показать списки')))   # ПОКАЗ СПИСКА
    dp.register_message_handler(insert_list)  # добавление нового списка в БД
