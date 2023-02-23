from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from create_bot import bot
from keyboard import kb_start
from funct import del_mess, msg_id_write, check_lists_numb, view_user_lists, list_or_thing
from action_flags import DelFlag_write
import sqlite3 as sq


async def del_list_button(message: types.Message):  # кнопка 'удалить список'
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


async def del_list(callback: types.CallbackQuery):  # удаление пунктов пользовательского списка
    global list_name
    id = callback.from_user.id  # посмотреть ID через коллбэки
    list_name = callback.data
    await del_mess(id)  # удаление предыдущего сообщения

    LoTFl = list_or_thing(id, list_name)  # проверяет список польз. списков или пункты внутри списка перед нами

    data_base = sq.connect('ListBotBase2.db')
    cur = data_base.cursor()
    DelFlag = cur.execute(f"SELECT DelFlag FROM flags WHERE user_id = {id}").fetchone()[0]
    if LoTFl and DelFlag == 1:  # если list_name - ПС и флаг удаления включен
        cur.execute(f'DELETE FROM lists WHERE list = ? AND user_id = ?', (list_name, id))
        data_base.commit()
        msg = await bot.send_message(callback.from_user.id, f'Список "{list_name}" удален! ', reply_markup=kb_start)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        DelFlag = 0
        DelFlag_write(DelFlag, id)  # запись DelFlag  в БД


def register_del_list_handlers(dp: Dispatcher):
    dp.register_message_handler(del_list_button, (Text(equals='удалить список')))  # удаление списка
    dp.register_callback_query_handler(del_list)  # просмотр пунктов пользовательского списка
