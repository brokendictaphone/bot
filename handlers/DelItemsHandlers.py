from aiogram import types, Dispatcher
from create_bot import bot
from keyboard import kb_start
from funct import del_mess, msg_id_write, list_or_thing, check_user_list, view_list
import sqlite3 as sq


async def del_item(callback: types.CallbackQuery):  # кнопка 'удалить список'
    global list_name
    id = callback.from_user.id  # посмотреть ID через коллбэки
    ThingAddFl_write(1, id)
    list_name = callback.data
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
                await bot.send_message(callback.from_user.id,'text', reply_markup=kb_start)  # клавиатура стартовая
                msg_id_write(msg, id)  # записывает айди сообщения в БД
            else:
                await callback.answer('Похоже, список пуст.', show_alert=True)
                msg = await bot.send_message(callback.from_user.id, 'Напишите, что нужно добавить в список?', reply_markup=kb_start)
                msg_id_write(msg, id)  # записывает айди сообщения в БД

    else:   # если list_name - пункт в пользовательском списке(УДАЛЕНИЕ)
        data_base = sq.connect('ListBotBase2.db')  # связь с БД
        cur = data_base.cursor()
        user_list_name = \
        cur.execute("SELECT list FROM lists WHERE user_id = ? AND thing = ?", (id, list_name)).fetchone()[0]  # имя ПС
        cur.execute(f'DELETE FROM lists WHERE thing = ? AND user_id = ?', (callback.data, id))
        data_base.commit()
        # await del_mess(id)  # удаление предыдущего сообщения
        flag = check_thing_in_data_base(user_list_name, id)  # проверяет, есть ли пункты в ПС
        if flag:
            list_kb = view_list(id,user_list_name)  # функция создает и возвращет список дел в виде клавиатуры
            msg = await bot.send_message(callback.from_user.id, 'Дельце-то сделано!', reply_markup=list_kb)
            await bot.send_message(callback.from_user.id,'text', reply_markup=kb_start)  # клавиатура стартовая
            msg_id_write(msg, id)  # записывает айди сообщения в БД
        else:
            await callback.answer(f'Похоже, все дела из списка "{user_list_name}" переделаны. Мои поздравления!', show_alert=True)
            msg = await bot.send_message(callback.from_user.id, 'Продолжим?', reply_markup=kb_start)
            msg_id_write(msg, id)  # записывает айди сообщения в БД

def register_del_item_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(del_item)  # удаление пунктов пользовательского списка