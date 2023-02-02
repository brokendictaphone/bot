import sqlite3 as sq
from create_bot import bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


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

# ниже функции для удаления сообщений
async def del_mess(id):
    """удаляет сообщения бота по месседж айди"""
    data_base = sq.connect('ListBotBase2.db')  # связь с БД
    cur = data_base.cursor()
    for msg_id in cur.execute(f"SELECT msg FROM msg_ids WHERE user_id = {id}"):
        await bot.delete_message(id, msg_id[0])
    data_base.close()  # закрытие ДБ


def msg_id_write(msg, id):
    """записывает id сообщения в БД"""
    data_base = sq.connect('ListBotBase2.db')  # добавление данных в список дел
    cur = data_base.cursor()
    cur.execute(f"SELECT msg FROM msg_ids WHERE user_id = {id} ")  # выбор значения
    if cur.fetchone():
        cur.execute(f'UPDATE msg_ids SET msg = {msg.message_id} WHERE user_id = {id}')
    else:
        cur.execute("""INSERT INTO msg_ids(user_id,msg) VALUES(?,?)""",
                    (id, msg.message_id))  # добавление данных
    data_base.commit()  # подтверждение действий
    data_base.close()  # закрытие ДБ


def check_data_base(id):
    """проверяет, есть ли записи у пользователя в БД"""
    check_list = []
    flag = False
    data_base = sq.connect('ListBotBase2.db')  # связь с БД
    cur = data_base.cursor()
    for lists in cur.execute(f"SELECT list FROM lists WHERE user_id = {id}"):  # вывод данных из БД(выбрать всё из таблицы пользователи
        check_list.append(lists)
    if check_list:
        flag = True
    check_list.clear()
    return flag