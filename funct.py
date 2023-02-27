import sqlite3 as sq
from create_bot import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def del_mess(id):
    """удаляет сообщения бота по месседж айди"""
    data_base = sq.connect('ListBotBase2.db')  # связь с БД
    cur = data_base.cursor()
    cur.execute(f"SELECT msg FROM msg_ids WHERE user_id = {id}")
    msg_list = cur.fetchall()
    for msg_id in msg_list:
        await bot.delete_message(id, msg_id[0])
        cur.execute(f'DELETE FROM msg_ids WHERE msg = ? AND user_id = ?', (msg_id[0], id))
    data_base.commit()  # подтверждение действий
    data_base.close()  # закрытие ДБ


def msg_id_write(msg, id):
    """записывает id сообщения в БД"""
    data_base = sq.connect('ListBotBase2.db')  # добавление данных в список дел
    cur = data_base.cursor()
    cur.execute("""INSERT INTO msg_ids(user_id,msg) VALUES(?,?)""", (id, msg.message_id))  # добавление данных
    data_base.commit()  # подтверждение действий
    data_base.close()  # закрытие ДБ


def current_list_write(list_name, id):
    """записывает название текущего списка в БД"""
    data_base = sq.connect('ListBotBase2.db')
    cur = data_base.cursor()
    cur.execute(f"SELECT list_name FROM current_list WHERE user_id = {id} ")  # выбор значения
    if cur.fetchone():
        cur.execute(f'UPDATE current_list SET list_name = "{list_name}" WHERE user_id = {id}')  # !!!КАВЫЧКИ!!!
    else:
        cur.execute("""INSERT INTO current_list (user_id,list_name) VALUES(?,?)""", (id, list_name))
    data_base.commit()  # подтверждение действий
    data_base.close()  # закрытие ДБ


def check_data_base(id):
    """проверяет, есть ли записи у пользователя в БД"""
    flag = False
    data_base = sq.connect('ListBotBase2.db')  # связь с БД
    cur = data_base.cursor()
    res = cur.execute(f"SELECT list FROM lists WHERE user_id = {id}")  # вывод данных из БД(выбрать всё из таблицы пользователи
    if len(res.fetchall()) > 0:
        flag = True
    return flag


def check_thing_in_data_base(user_list_name, id):
    """проверяет, есть ли пункты в ПС"""
    flag = False
    data_base = sq.connect('ListBotBase2.db')  # связь с БД
    cur = data_base.cursor()
    res = cur.execute("SELECT thing FROM lists WHERE list = ? AND user_id = ? ", (user_list_name, id))  # вывод данных из БД(выбрать всё из таблицы пользователи
    if len(res.fetchall()) > 1:
        flag = True
    return flag


def check_lists_numb(id):
    """проверка количества списков"""
    data_base = sq.connect('ListBotBase2.db')  # связь с БД
    cur = data_base.cursor()
    res = cur.execute(f"SELECT DISTINCT list FROM lists WHERE user_id = {id}")  # вывод данных из БД(выбрать всё из таблицы пользователи)
    length = len(res.fetchall())
    return length


def view_user_lists(id):
    """создает и возвращет пользовательские списки в виде клавиатуры"""
    list_kb = InlineKeyboardMarkup()  # создание клавиатуры списка
    data_base = sq.connect('ListBotBase2.db')  # связь с БД
    cur = data_base.cursor()
    list = cur.execute(f"SELECT DISTINCT list FROM lists WHERE user_id = {id}")  # вывод данных из БД(выбрать всё из таблицы )
    for tpl in list.fetchall():
        b = InlineKeyboardButton(tpl[0], callback_data=tpl[0])
        list_kb.row(b)
    return list_kb


def check_user_list(id, list_name):
    """проверяет, есть ли пункты в пользовательском списке"""
    flag = False
    data_base = sq.connect('ListBotBase2.db')  # связь с БД
    cur = data_base.cursor()
    res = cur.execute("SELECT thing FROM lists WHERE user_id = ? AND list = ?", (id, list_name))  # вывод данных из БД(выбрать всё из таблицы пользователи
    if len(res.fetchall()) > 1:  # если в списке есть хотя бы одна не пустая запись
        flag = True
    return flag


def list_or_thing(id, check_name):
    """проверяет, входит ли запись в пользовательские списки"""
    LoTFl = False
    data_base = sq.connect('ListBotBase2.db')  # связь с БД
    cur = data_base.cursor()
    res = cur.execute(f"SELECT DISTINCT list FROM lists WHERE user_id = {id}")  # вывод данных из БД(выбрать всё из таблицы пользователи)
    for tpl in res.fetchall():
        if tpl[0] == check_name:
            LoTFl = True
    return LoTFl


def view_list(id, list_name):
    """создает и возвращет список дел в виде клавиатуры"""
    list_kb = InlineKeyboardMarkup()  # создание клавиатуры списка
    data_base = sq.connect('ListBotBase2.db')  # связь с БД
    cur = data_base.cursor()
    for things in cur.execute("SELECT thing FROM lists WHERE user_id = ? AND list = ?", (id, list_name)):  # вывод данных из БД(выбрать всё из таблицы пользователи)
        for thing in things:
            if thing is None:  # "отфильтровывает" первый пустой пункт
                continue
            else:
                b = InlineKeyboardButton(thing, callback_data=thing)
                list_kb.row(b)
    return list_kb
