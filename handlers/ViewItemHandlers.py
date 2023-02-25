from aiogram import types, Dispatcher
from create_bot import bot
from FSMachine import FSMStates
from keyboard import manage_list_kbrd
from funct import del_mess, msg_id_write, check_user_list, view_list
import sqlite3 as sq


async def view_items_in_list(callback: types.CallbackQuery):  # просмотр пунктов пользовательского списка
    id = callback.from_user.id  # посмотреть ID через коллбэки
    list_name = callback.data
    data_base = sq.connect('ListBotBase2.db')
    cur = data_base.cursor()
    cur.execute(f"SELECT list_name FROM current_list WHERE user_id = {id} ")  # выбор значения
    if cur.fetchone():
        cur.execute(f'UPDATE current_list SET list_name = "{callback.data}" WHERE user_id = {id}')  # !!!КАВЫЧКИ!!!
    else:
        cur.execute("""INSERT INTO current_list (user_id,list_name) VALUES(?,?)""", (id, callback.data))
    data_base.commit()
    data_base.close()

    await del_mess(id)  # удаление предыдущего сообщения
    flag = check_user_list(id, list_name)  # проверяет, есть ли пункты в пользовательском списке?
    if flag:  # если ПС не пуст
        list_kb = view_list(id, list_name)  # функция создает пункты пользовательских списков в виде клавиатуры
        msg = await bot.send_message(callback.from_user.id, f'Список "{list_name}": ', reply_markup=list_kb)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        msg2 = await bot.send_message(callback.from_user.id, 'Напишите, что нужно добавить?', reply_markup=manage_list_kbrd)  # клавиатура стартовая
        msg_id_write(msg2, id)  # записывает айди сообщения в БД
        await FSMStates.add_item.set() # состояние "создать пункт в ПС"
    else:
        await callback.answer('Похоже, список пуст.', show_alert=True)
        msg = await bot.send_message(callback.from_user.id, 'Напишите, что нужно добавить в список?', reply_markup=manage_list_kbrd)
        await FSMStates.add_item.set()  # включено состояние "создать пункт в ПС"
        msg_id_write(msg, id)  # записывает айди сообщения в БД


def register_view_item_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(view_items_in_list)  # просмотр пунктов пользовательского списка
