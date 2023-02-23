from aiogram import types
from keyboard import kb_start
from funct import del_mess, msg_id_write, check_data_base, view_user_lists
from flags import ThingAddFl_write


async def view_lists_button(message: types.Message):  # кнопка показать списки
    id = message.chat.id
    ThingAddFl_write(0, id)  # выключение режима записи нового пункта в БД ПС(запись флага в БД)
    await del_mess(id)  # удаление предыдущего сообщения
    flag = check_data_base(id)
    if flag:
        list_kb = view_user_lists(id)  # функция создает и возвращет списки пользователя в виде клавиатуры
        msg = await message.answer('Актуальные списки: ', reply_markup=list_kb)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        msg = await message.answer('для обычной клавиатуры ', reply_markup=kb_start)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя
    else:
        msg = await message.answer('Нечего показать-то! Ни одного списка не создано...', reply_markup=kb_start)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя
