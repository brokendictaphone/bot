import sqlite3 as sq
from create_bot import bot


async def del_mess(id):
    """удаляет сообщения бота по месседж айди"""
    data_base = sq.connect('ListBotBase2.db')  # связь с БД
    cur = data_base.cursor()
 #   for msg_id in cur.execute(f"SELECT msg FROM msg_ids WHERE user_id = {id}"):
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
    cur.execute("""INSERT INTO msg_ids(user_id,msg) VALUES(?,?)""",
                    (id, msg.message_id))  # добавление данных
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
