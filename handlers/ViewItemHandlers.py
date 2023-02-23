from aiogram import types, Dispatcher
from create_bot import bot
from keyboard import kb_start
from funct import del_mess, msg_id_write, list_or_thing, check_user_list, view_list
import sqlite3 as sq


async def view_thing_in_list(callback: types.CallbackQuery):  # просмотр пунктов пользовательского списка
    id = callback.from_user.id  # посмотреть ID через коллбэки
    list_name = callback.data
    await del_mess(id)  # удаление предыдущего сообщения
    flag = check_user_list(id, list_name)  # проверяет, есть ли пункты в пользовательском списке?
    LoTFl = list_or_thing(id, list_name)  # проверяет список польз. списков или пункты внутри списка перед нами
    data_base = sq.connect('ListBotBase2.db')
    cur = data_base.cursor()
    DelFlag = cur.execute(f"SELECT DelFlag FROM flags WHERE user_id = {id}").fetchone()[0]
    data_base.close()
    if LoTFl and DelFlag == 0:  # если list_name - ПС и флаг удаления выключен
        if flag:  # если ПС не пуст
            list_kb = view_list(id, list_name)  # функция создает пункты пользовательских списков в виде клавиатуры
            msg = await bot.send_message(callback.from_user.id, f'Список "{list_name}": ', reply_markup=list_kb)
            await bot.send_message(callback.from_user.id, 'text', reply_markup=kb_start)  # клавиатура стартовая
            msg_id_write(msg, id)  # записывает айди сообщения в БД
        else:
            await callback.answer('Похоже, список пуст.', show_alert=True)
            msg = await bot.send_message(callback.from_user.id, 'Напишите, что нужно добавить в список?', reply_markup=kb_start)
            msg_id_write(msg, id)  # записывает айди сообщения в БД


def register_view_item_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(view_thing_in_list)  # просмотр пунктов пользовательского списка
