from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from FSMachine import FSMStates
from keyboard import kb_start
from funct import *
from action_flags import *
import sqlite3 as sq


async def add_list_button(message: types.Message):  # кнопка создать список
    id = message.chat.id
    await del_mess(id)  # удаление предыдущего сообщения
    list_len = check_lists_numb(id)  # проверка количества польовательских списков
    ThingAddFl_write(0, id)  # выключение режима записи нового пункта в БД ПС(запись флага в БД)
    if list_len < 3:
        msg = await message.answer('Введите название нового списка: ')
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя
        await FSMStates.add_list.set()  # включено состояние "создать ПС"
    else:
        msg = await message.answer('Нельзя создать больше 3 списков!', reply_markup=kb_start)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя


async def add_list(message: types.Message, state: FSMContext):  # создание ПС
    id = message.chat.id
    await del_mess(id)  # удаление предыдущего сообщения
    data_base = sq.connect('ListBotBase2.db')
    cur = data_base.cursor()
    cur.execute("""INSERT INTO lists VALUES(?,?,?)""", (id, message.text, None))  # добавление нового списка
    data_base.commit()  # подтверждение действий
    data_base.close()
    msg = await message.answer(f'Вот и создан список "{message.text}"', reply_markup=kb_start)
    msg_id_write(msg, id)  # записывает айди сообщения в БД
    await message.delete()  # удалить сообщение пользователя
    await state.finish()  # выключение машины состояний



async def prompt_mess(message: types.Message):  # подсказка
    id = message.chat.id
    await del_mess(id)  # удаление предыдущего сообщения
    msg = await message.answer(f'Сначала нужно нажать кнопку "создать список"!', reply_markup=kb_start)
    msg_id_write(msg, id)  # записывает айди сообщения в БД
    await message.delete()  # удалить сообщение пользователя

#
# async def insert_smth(message: types.Message):
#     id = message.chat.id
#     await del_mess(id)  # удаление предыдущего сообщения
#     data_base = sq.connect('ListBotBase2.db')
#     cur = data_base.cursor()
#     AddFlag = cur.execute(f"SELECT AddFlag FROM flags WHERE user_id = {id}").fetchone()[0]
#     ThingAddFl = cur.execute(f"SELECT ThingAddFl FROM flags WHERE user_id = {id}").fetchone()[0]
#     if ThingAddFl == 0:
#         if AddFlag == 1:
#             cur.execute("""INSERT INTO lists VALUES(?,?,?)""", (id, message.text, None))  # добавление нового списка
#             data_base.commit()  # подтверждение действий
#             msg = await message.answer(f'Вот и создан список "{message.text}"', reply_markup=kb_start)
#             msg_id_write(msg, id)  # записывает айди сообщения в БД
#             await message.delete()  # удалить сообщение пользователя
#             AddFlag = 0
#             AddFlag_write(AddFlag, id)  # запись AddFlag в БД
#         else:
#             if message.text == 'показать списки':
#                 pass
#             else:
#                 msg = await message.answer(f'Сначала нужно нажать кнопку "создать список"!', reply_markup=kb_start)
#                 msg_id_write(msg, id)  # записывает айди сообщения в БД
#                 await message.delete()  # удалить сообщение пользователя
#     else:
#         if '"' in message.text:
#             msg = await message.answer('Нельзя использовать кавычки! Введи без них')
#             msg_id_write(msg, id)  # записывает айди сообщения в БД
#             await message.delete()  # удалить сообщение пользователя
#         elif len(message.text) > 25:
#             msg = await message.answer('Слишком длинно, не возьмусь')
#             msg_id_write(msg, id)  # записывает айди сообщения в БД
#             await message.delete()  # удалить сообщение пользователя
#         else:
#             cur.execute("""INSERT INTO lists VALUES(?,?,?)""",
#                         (id, list_name, message.text))  # добавление данных в список дел
#             data_base.commit()  # подтверждение действий
#             await del_mess(id)  # удаление предыдущего сообщения
#             list_kb = view_list(id, list_name)  # функция создает пункты пользовательских списков в виде клавиатуры
#             msg = await message.answer(f'Вот и добавили "{message.text}" в список. Добавим ещё что-то?', reply_markup=list_kb)
#             msg_id_write(msg, id)  # записывает айди сообщения в БД
#             msg2 = await message.answer(f'Что ещё нужно добавить в список?', reply_markup=kb_start)  # клавиатура стартовая
#             msg_id_write(msg2, id)  # записывает айди сообщения в БД
#             await message.delete()  # удалить сообщение пользователя
#
#
# async def view_thing_in_list(callback: types.CallbackQuery):  # просмотр пунктов пользовательского списка
#     global list_name
#     id = callback.from_user.id  # посмотреть ID через коллбэки
#     ThingAddFl_write(1, id)
#     list_name = callback.data
#     await del_mess(id)  # удаление предыдущего сообщения
#
#     flag = check_user_list(id, list_name)  # проверяет, есть ли пункты в пользовательском списке?
#     LoTFl = list_or_thing(id, list_name)  # проверяет список польз. списков или пункты внутри списка перед нами
#
#     data_base = sq.connect('ListBotBase2.db')
#     cur = data_base.cursor()
#     DelFlag = cur.execute(f"SELECT DelFlag FROM flags WHERE user_id = {id}").fetchone()[0]
#     if LoTFl:  # если list_name - пользовательский список
#         if DelFlag:  # удаление списка
#             cur.execute(f'DELETE FROM lists WHERE list = ? AND user_id = ?', (list_name, id))
#             data_base.commit()
#             msg = await bot.send_message(callback.from_user.id, f'Список "{list_name}" удален! ', reply_markup=kb_start)
#             msg_id_write(msg, id)  # записывает айди сообщения в БД
#             DelFlag = 0
#             DelFlag_write(DelFlag, id)  # запись DelFlag  в БД
#         else:
#             if flag:  # если в ПС не пуст
#                 list_kb = view_list(id, list_name)  # функция создает пункты пользовательских списков в виде клавиатуры
#                 msg = await bot.send_message(callback.from_user.id, f'Список "{list_name}": ', reply_markup=list_kb)
#                 await bot.send_message(callback.from_user.id,'text', reply_markup=kb_start)  # клавиатура стартовая
#                 msg_id_write(msg, id)  # записывает айди сообщения в БД
#             else:
#                 await callback.answer('Похоже, список пуст.', show_alert=True)
#                 msg = await bot.send_message(callback.from_user.id, 'Напишите, что нужно добавить в список?', reply_markup=kb_start)
#                 msg_id_write(msg, id)  # записывает айди сообщения в БД
#
#     else:   # если list_name - пункт в пользовательском списке(УДАЛЕНИЕ)
#         data_base = sq.connect('ListBotBase2.db')  # связь с БД
#         cur = data_base.cursor()
#         user_list_name = \
#         cur.execute("SELECT list FROM lists WHERE user_id = ? AND thing = ?", (id, list_name)).fetchone()[0]  # имя ПС
#         cur.execute(f'DELETE FROM lists WHERE thing = ? AND user_id = ?', (callback.data, id))
#         data_base.commit()
#         # await del_mess(id)  # удаление предыдущего сообщения
#         flag = check_thing_in_data_base(user_list_name, id)  # проверяет, есть ли пункты в ПС
#         if flag:
#             list_kb = view_list(id,user_list_name)  # функция создает и возвращет список дел в виде клавиатуры
#             msg = await bot.send_message(callback.from_user.id, 'Дельце-то сделано!', reply_markup=list_kb)
#             await bot.send_message(callback.from_user.id,'text', reply_markup=kb_start)  # клавиатура стартовая
#             msg_id_write(msg, id)  # записывает айди сообщения в БД
#         else:
#             await callback.answer(f'Похоже, все дела из списка "{user_list_name}" переделаны. Мои поздравления!', show_alert=True)
#             msg = await bot.send_message(callback.from_user.id, 'Продолжим?', reply_markup=kb_start)
#             msg_id_write(msg, id)  # записывает айди сообщения в БД


def register_AddLIst_handlers(dp: Dispatcher):
    dp.register_message_handler(add_list_button, (Text(equals='создать список')), state=None)  # кнопка "создать список"
    dp.register_message_handler(add_list, state=FSMStates.add_list)  # создание списка
    dp.register_message_handler(prompt_mess, state=None)  # подсказка



