from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3 as sq


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


# @dp.message_handler(Text(equals='показать список'))  # ПОКАЗ СПИСКА
# async def add_button(message: types.Message):
#     id = message.chat.id
#     await del_mess(id)  # удаление предыдущего сообщения
#     flag = check_data_base(id)
#     if flag:
#         list_kb = view_list(id)  # функция создает и возвращет список дел в виде клавиатуры
#         msg = await message.answer('Актуальный список: ', reply_markup=list_kb)
#         msg_id_write(msg, id)  # записывает айди сообщения в БД
#         await message.delete()  # удалить сообщение пользователя
#     else:
#         msg = await message.answer('Нечего показать-то! Список пока пуст...', reply_markup=kb_start)
#         msg_id_write(msg, id)  # записывает айди сообщения в БД
#         await message.delete()  # удалить сообщение пользователя


# @dp.message_handler()  # добавление в список
# async def insert_item(message: types.Message):
#     id = message.chat.id
#     await del_mess(id)  # удаление предыдущего сообщения
#     data_base = sq.connect('ListBotBase2.db')  # добавление данных в список дел
#     cur = data_base.cursor()
#     if '"' in message.text:
#         msg = await message.answer('Нельзя использовать кавычки! Введи без них')
#         msg_id_write(msg, id)  # записывает айди сообщения в БД
#     elif len(message.text) > 25:
#         msg = await message.answer('Слишком длинно, не возьмусь')
#         msg_id_write(msg, id)  # записывает айди сообщения в БД
#     else:
#         cur.execute("""INSERT INTO things VALUES(?,?)""", (id, message.text))  # добавление данных в список дел
#         data_base.commit()  # подтверждение действий
#         msg = await message.answer(f'Вот и добавили "{message.text}" в список дел', reply_markup=kb_start)
#         msg_id_write(msg, id)  # записывает айди сообщения в БД
#         await message.delete()  # удалить сообщение пользователя

#
# @dp.callback_query_handler()
# async def del_thing(callback: types.CallbackQuery):
#     id = callback.from_user.id  # посмотреть ID через коллбэки
#     data_base = sq.connect('ListBotBase2.db')  # связь с БД
#     cur = data_base.cursor()
#     cur.execute(f'DELETE FROM things WHERE thing = "{callback.data}" AND user_id = {id}')
#     data_base.commit()
#     await bot.delete_message(callback.from_user.id, callback.message.message_id)  # удаление предыдущего сообщения бота
#
#     flag = check_data_base(id)
#     if flag:
#         list_kb = view_list(id)  # функция создает и возвращет список дел в виде клавиатуры
#         await callback.answer('Дельце-то сделано!', show_alert=True)
#         msg = await bot.send_message(callback.from_user.id, 'Актуальный список: ', reply_markup=list_kb)
#         msg_id_write(msg, id)  # записывает айди сообщения в БД
#     else:
#         await callback.answer('Похоже, все дела переделаны. Мои поздравления!', show_alert=True)
#         msg = await bot.send_message(callback.from_user.id, 'Продолжим?', reply_markup=kb_start)
#         msg_id_write(msg, id)  # записывает айди сообщения в БД
