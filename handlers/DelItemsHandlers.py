from aiogram import types, Dispatcher
from create_bot import bot
from keyboard import manage_list_kbrd, cancel_del_kbrd
from FSMachine import FSMStates
from funct import del_mess, msg_id_write, view_list, check_thing_in_data_base
import sqlite3 as sq


async def del_item(callback: types.CallbackQuery):  # удаление пункта в списке
    id = callback.from_user.id  # посмотреть ID через коллбэки
    item_name = callback.data
    await del_mess(id)  # удаление предыдущего сообщения
    data_base = sq.connect('ListBotBase2.db')  # связь с БД
    cur = data_base.cursor()
    user_list_name = \
    cur.execute("SELECT list FROM lists WHERE user_id = ? AND thing = ?", (id, item_name )).fetchone()[0]  # имя ПС
    cur.execute(f'DELETE FROM lists WHERE thing = ? AND user_id = ? AND list = ?', (item_name , id, user_list_name))
    data_base.commit()
    flag = check_thing_in_data_base(user_list_name, id)  # проверяет, есть ли пункты в ПС
    if flag:
        list_kb = view_list(id, user_list_name)  # функция создает и возвращет список дел в виде клавиатуры
        msg = await bot.send_message(callback.from_user.id,
                                     'Дельце-то сделано!', reply_markup=list_kb)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        msg2 = await bot.send_message(callback.from_user.id,
                                      'Удалим ещё что-то?', reply_markup=cancel_del_kbrd)  # клавиатура стартовая
        msg_id_write(msg2, id)  # записывает айди сообщения в БД
    else:
        await callback.answer(f'Похоже, все дела из списка "{user_list_name}" переделаны.'
                              f' Мои поздравления!', show_alert=True)
        msg = await bot.send_message(callback.from_user.id, 'Продолжим?', reply_markup=manage_list_kbrd)
        msg_id_write(msg, id)  # записывает айди сообщения в БД


def register_del_item_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(del_item, state=FSMStates.del_item)  # удаление пунктов пользовательского списка
