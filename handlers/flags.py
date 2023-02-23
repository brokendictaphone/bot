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
