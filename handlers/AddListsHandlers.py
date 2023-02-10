from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from keyboard import kb_start
from funct import *
from things_add import *
import sqlite3 as sq
ThingAddFl = 0

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


def DelFlag_write(delflag, id):
    """записывает DelFlag в БД"""
    data_base = sq.connect('ListBotBase2.db')  # добавление данных в список дел
    cur = data_base.cursor()
    cur.execute(f"SELECT DelFlag FROM flags WHERE user_id = {id} ")  # выбор значения
    if cur.fetchone():
        cur.execute(f'UPDATE flags SET DelFlag = {delflag} WHERE user_id = {id}')
    else:
        cur.execute("""INSERT INTO flags(user_id,DelFlag) VALUES(?,?)""",
                    (id, delflag))  # добавление данных
    data_base.commit()  # подтверждение действий
    data_base.close()  # закрытие ДБ


def ThingAddFl_write(thingaddfl, id):
    """записывает ThingAddFl в БД"""
    data_base = sq.connect('ListBotBase2.db')  # добавление пункта в пользовательский список дел
    cur = data_base.cursor()
    cur.execute(f"SELECT ThingAddFl FROM flags WHERE user_id = {id} ")  # выбор значения
    if cur.fetchone():
        cur.execute(f'UPDATE flags SET ThingAddFl = {thingaddfl} WHERE user_id = {id}')
    else:
        cur.execute("""INSERT INTO flags(user_id,ThingAddFl) VALUES(?,?)""",
                    (id, thingaddfl))  # добавление данных
    data_base.commit()  # подтверждение действий
    data_base.close()  # закрытие ДБ
def view_user_lists(id):
    """создает и возвращет пользовательские списки в виде клавиатуры"""
    list_kb = InlineKeyboardMarkup()  # создание клавиатуры списка
    data_base = sq.connect('ListBotBase2.db')  # связь с БД
    cur = data_base.cursor()
    list  = cur.execute(f"SELECT DISTINCT list FROM lists WHERE user_id = {id}")  # вывод данных из БД(выбрать всё из таблицы )
    for tpl in list.fetchall():
        b = InlineKeyboardButton(tpl[0], callback_data=tpl[0])
        list_kb.row(b)
    return list_kb


def check_lists_numb(id):
    """проверка количества списков"""
    data_base = sq.connect('ListBotBase2.db')  # связь с БД
    cur = data_base.cursor()
    res = cur.execute(f"SELECT DISTINCT list FROM lists WHERE user_id = {id}") # вывод данных из БД(выбрать всё из таблицы пользователи)
    length = len(res.fetchall())
    return length


def list_or_thing(id, check_name):
    """проверяет, входит ли запись в пользовательские списки"""
    LoTFl = False
    data_base = sq.connect('ListBotBase2.db')  # связь с БД
    cur = data_base.cursor()
    res = cur.execute(f"SELECT DISTINCT list FROM lists WHERE user_id = {id}") # вывод данных из БД(выбрать всё из таблицы пользователи)
    for tpl in res.fetchall():
        if tpl[0] == check_name:
            LoTFl = True
    return LoTFl



def check_user_list(id, list_name):
    """проверяет, есть ли пункты в пользовательском списке"""
    flag = False
    data_base = sq.connect('ListBotBase2.db')  # связь с БД
    cur = data_base.cursor()
    res = cur.execute("SELECT thing FROM lists WHERE user_id = ? AND list = ?", (id, list_name))  # вывод данных из БД(выбрать всё из таблицы пользователи
    if len(res.fetchall()) > 1:  # если в списке есть хотя бы одна не пустая запись
        flag = True
    return flag


async def add_list(message: types.Message):  # кнопка создать список
    global ThingAddFl
    id = message.chat.id
    await del_mess(id)  # удаление предыдущего сообщения
    list_len = check_lists_numb(id)  # проверка количества польовательских списков
    ThingAddFl = 0
    if list_len < 3:
        msg = await message.answer('Введите название нового списка: ')
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя
        AddFlag = 1  # разрешение на добавление пользовательского списка в БД
        AddFlag_write(AddFlag, id)  # запись AddFlag в БД
    else:
        msg = await message.answer('Нельзя создать больше 3 списков!', reply_markup=kb_start)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя
        AddFlag = 0
        AddFlag_write(AddFlag, id)  # запись AddFlag в БД


async def del_list(message: types.Message):  # кнопка 'удалить список'
    # AddFlag_write(0, id)  # запись AddFlag в БД
    # ThingAddFl_write(0,id)  # запись ThingAddFl в БД
    id = message.chat.id
    await del_mess(id)  # удаление предыдущего сообщения
    list_len = check_lists_numb(id)  # проверка количества польовательских списков
    if list_len > 0:
        DelFlag = 1
        DelFlag_write(DelFlag, id)  # запись DelFlag  в БД
        list_kb = view_user_lists(id)
        msg = await message.answer('Какой список следует удалить?', reply_markup=list_kb)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя
    else:
        DelFlag = 0
        DelFlag_write(DelFlag, id)  # запись DelFlag  в БД
        msg = await message.answer('Да ведь нечего удалить-то!', reply_markup=kb_start)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя


async def insert_smth(message: types.Message):
    id = message.chat.id
    await del_mess(id)  # удаление предыдущего сообщения
    data_base = sq.connect('ListBotBase2.db')
    cur = data_base.cursor()
    AddFlag = cur.execute(f"SELECT AddFlag FROM flags WHERE user_id = {id}").fetchone()[0]
    if ThingAddFl == 0:
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
    else:
        if '"' in message.text:
            msg = await message.answer('Нельзя использовать кавычки! Введи без них')
            msg_id_write(msg, id)  # записывает айди сообщения в БД
        elif len(message.text) > 25:
            msg = await message.answer('Слишком длинно, не возьмусь')
            msg_id_write(msg, id)  # записывает айди сообщения в БД
        else:
            cur.execute("""INSERT INTO lists VALUES(?,?,?)""",
                        (id, list_name, message.text))  # добавление данных в список дел
            data_base.commit()  # подтверждение действий
            list_kb = view_list(id, list_name)  # функция создает пункты пользовательских списков в виде клавиатуры
            msg = await message.answer(f'Вот и добавили "{message.text}" в список', reply_markup=list_kb)

            await message.answer(f'Что ещё нужно добавить в список?', reply_markup=kb_start)
            msg_id_write(msg, id)  # записывает айди сообщения в БД
            await message.delete()  # удалить сообщение пользователя

async def view_lists_button(message: types.Message):  # кнопка показать списки
    global ThingAddFl
    ThingAddFl = 0
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


async def view_thing_in_list(callback: types.CallbackQuery):  # просмотр пунктов пользовательского списка
    global ThingAddFl, list_name
    ThingAddFl = 1
    list_name = callback.data
    id = callback.from_user.id  # посмотреть ID через коллбэки
    await del_mess(id)  # удаление предыдущего сообщения

    flag = check_user_list(id, list_name)  # проверяет, есть ли пункты в пользовательском списке?
    LoTFl = list_or_thing(id, list_name)  # проверяет список польз. списков или пункты внутри списка перед нами

    data_base = sq.connect('ListBotBase2.db')
    cur = data_base.cursor()
    DelFlag = cur.execute(f"SELECT DelFlag FROM flags WHERE user_id = {id}").fetchone()[0]
    if LoTFl:  # если list_name - пользовательский список
        if DelFlag:  # удаление списка
            cur.execute(f'DELETE FROM lists WHERE list = ? AND user_id = ?', (list_name, id))
            data_base.commit()
            msg = await bot.send_message(callback.from_user.id, f'Список "{list_name}" удален! ', reply_markup=kb_start)
            msg_id_write(msg, id)  # записывает айди сообщения в БД
            DelFlag = 0
            DelFlag_write(DelFlag, id)  # запись DelFlag  в БД
        else:
            if flag:  # если в ПС не пуст
                list_kb = view_list(id, list_name)  # функция создает пункты пользовательских списков в виде клавиатуры
                msg = await bot.send_message(callback.from_user.id, f'Список "{list_name}": ', reply_markup=list_kb)
                msg_id_write(msg, id)  # записывает айди сообщения в БД
            else:
                await callback.answer('Похоже, список пуст.', show_alert=True)
                msg = await bot.send_message(callback.from_user.id, 'Напишите, что нужно добавить в список?', reply_markup=kb_start)
                msg_id_write(msg, id)  # записывает айди сообщения в БД

    else:   # если list_name - пункт в пользовательском списке(УДАЛЕНИЕ)
        data_base = sq.connect('ListBotBase2.db')  # связь с БД
        cur = data_base.cursor()
        cur.execute(f'DELETE FROM lists WHERE thing = ? AND user_id = ?', (callback.data, id))
        data_base.commit()
        #await del_mess(id)  # удаление предыдущего сообщения
        flag = check_data_base(id)
        if flag:
            list_kb = view_list(id,list_name)  # функция создает и возвращет список дел в виде клавиатуры
            msg = await bot.send_message(callback.from_user.id, 'Дельце-то сделано!', reply_markup=kb_start)
            msg_id_write(msg, id)  # записывает айди сообщения в БД
        else:
            await callback.answer('Похоже, все дела переделаны. Мои поздравления!', show_alert=True)
            msg = await bot.send_message(callback.from_user.id, 'Продолжим?', reply_markup=kb_start)
            msg_id_write(msg, id)  # записывает айди сообщения в БД


def register_AddLIst_handlers(dp: Dispatcher):
    dp.register_message_handler(add_list, (Text(equals='создать список')))  # создание списка
    dp.register_message_handler(del_list, (Text(equals='удалить список')))  # удаление списка
    dp.register_message_handler(view_lists_button, (Text(equals='показать списки')))   # показ списков
    dp.register_message_handler(insert_smth)  # добавление пользовательских списков и пунктов в них
    dp.register_callback_query_handler(view_thing_in_list)  # просмотр пунктов пользовательского списка



