from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from FSMachine import FSMStates
from aiogram import types, Dispatcher
from create_bot import bot
from keyboard import kb_start
from funct import del_mess, msg_id_write, check_lists_numb, view_user_lists
import sqlite3 as sq


async def del_list_button(message: types.Message):  # кнопка 'удалить список'
    id = message.chat.id
    await del_mess(id)  # удаление предыдущего сообщения
    list_len = check_lists_numb(id)  # проверка количества польовательских списков
    if list_len > 0:
        await FSMStates.delete_list.set()  # включено состояние "удалить ПС"
        list_kb = view_user_lists(id)
        msg = await message.answer('Какой список следует удалить?', reply_markup=list_kb)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя
    else:
        msg = await message.answer('Да ведь нечего удалить-то!', reply_markup=kb_start)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя


async def del_list(callback: types.CallbackQuery, state: FSMContext):  # удаление пунктов пользовательского списка
    global list_name
    id = callback.from_user.id  # посмотреть ID через коллбэки
    list_name = callback.data
    await del_mess(id)  # удаление предыдущего сообщения
    data_base = sq.connect('ListBotBase2.db')
    cur = data_base.cursor()
    cur.execute(f'DELETE FROM lists WHERE list = ? AND user_id = ?', (list_name, id))
    data_base.commit()
    msg = await bot.send_message(callback.from_user.id, f'Список "{list_name}" удален! ', reply_markup=kb_start)
    msg_id_write(msg, id)  # записывает айди сообщения в БД
    await state.finish()  # выключение машины состояний



def register_del_list_handlers(dp: Dispatcher):
    dp.register_message_handler(del_list_button, (Text(equals='удалить список')), state=None)  # удаление списка
    dp.register_callback_query_handler(del_list, state=FSMStates.delete_list)  # просмотр пунктов пользовательского списка
