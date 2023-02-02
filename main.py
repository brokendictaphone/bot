from aiogram.utils import executor
from aiogram.dispatcher.filters import Text
from aiogram import types
from keyboard import kb_start
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from create_bot import dp, bot
import sqlite3 as sq


FrstMessFlag = True   # в значении Тру - первое сообщение, в значении Фалс - все последующие

data_base = sq.connect('ListBotBase.db')
cur = data_base.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS things (
    user_id INT,
    thing TXT
)""")   # создание таблицы в базе данных если она ещё не создана, в скобках указаны столбцы и тип данных в них

cur.execute("""CREATE TABLE IF NOT EXISTS msg_ids (
    user_id INT,
    msg NULL
)""")   # создание таблицы с мессадж айди, в скобках указаны столбцы и тип данных в них

data_base.commit()  # подтверждение действий
data_base.close()  # закрытие ДБ


def check_data_base(id):
    """проверяет, есть ли записи у пользователя в БД"""
    flag = False
    data_base = sq.connect('ListBotBase.db')  # связь с БД
    cur = data_base.cursor()
    res = cur.execute(f"SELECT thing FROM things WHERE user_id = {id}")  # вывод данных из БД(выбрать всё из таблицы пользователи
    if len(res.fetchall()) > 0:
        flag = True
    return flag


def view_list(id):
    """создает и возвращет список дел в виде клавиатуры"""
    list_kb = InlineKeyboardMarkup()  # создание клавиатуры списка
    data_base = sq.connect('ListBotBase.db')  # связь с БД
    cur = data_base.cursor()
    for things in cur.execute(f"SELECT thing FROM things WHERE user_id = {id}"):  # вывод данных из БД(выбрать всё из таблицы пользователи)
        for thing in things:
            b = InlineKeyboardButton(thing, callback_data=thing)
            list_kb.row(b)
    return list_kb


def msg_id_write(msg, id):
    """записывает id сообщения в БД"""
    data_base = sq.connect('ListBotBase.db')  # добавление данных в список дел
    cur = data_base.cursor()
    cur.execute(f"SELECT msg FROM msg_ids WHERE user_id = {id} ")  # выбор значения
    if cur.fetchone():
        cur.execute(f'UPDATE msg_ids SET msg = {msg.message_id} WHERE user_id = {id}')
    else:
        cur.execute("""INSERT INTO msg_ids(user_id,msg) VALUES(?,?)""",
                    (id, msg.message_id))  # добавление данных в список дел
    data_base.commit()  # подтверждение действий
    data_base.close()  # закрытие ДБ


async def del_mess(id):
    """удаляет сообщения бота по месседж айди"""
    data_base = sq.connect('ListBotBase.db')  # связь с БД
    cur = data_base.cursor()
    for msg_id in cur.execute(f"SELECT msg FROM msg_ids WHERE user_id = {id}"):
        await bot.delete_message(id, msg_id[0])
    data_base.close()  # закрытие ДБ


async def on_startup(_):  # служебное сообщение
    print('всё отлично: бот онлайн')


@dp.message_handler(commands=['start', 'help'])  # команда старт и кнопки
async def command_start(message: types.Message):
    global FrstMessFlag
    id = message.chat.id
    if not FrstMessFlag:
        await del_mess(id)  # удаление предыдущего сообщения
    msg = await bot.send_message(message.from_user.id, f'Привет, {message.chat.first_name.title()}!'
                                                 f' Я бот для составления списков, для того чтобы добавить что-нибудь'
                                                 f' в список, просто отправь это мне.'
                                                 f' Чтобы удалить что-то из списка, нажми на кнопку с названием этого что-то.'
                                                 f' Пожалуй, это всё, что нужно знать о моей работе))', reply_markup=kb_start)
    msg_id_write(msg, id)  # записывает айди сообщения в БД
    await message.delete()  # удалить сообщение пользователя
    FrstMessFlag = False


@dp.message_handler(Text(equals='показать список'))  # ПОКАЗ СПИСКА
async def add_button(message: types.Message):
    id = message.chat.id
    await del_mess(id)  # удаление предыдущего сообщения
    flag = check_data_base(id)
    if flag:
        list_kb = view_list(id)  # функция создает и возвращет список дел в виде клавиатуры
        msg = await message.answer('Актуальный список: ', reply_markup=list_kb)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя
    else:
        msg = await message.answer('Нечего показать-то! Список пока пуст...', reply_markup=kb_start)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя


@dp.message_handler()  # добавление в список
async def insert_item(message: types.Message):
    id = message.chat.id
    await del_mess(id)  # удаление предыдущего сообщения
    data_base = sq.connect('ListBotBase.db')  # добавление данных в список дел
    cur = data_base.cursor()
    if '"' in message.text:
        msg = await message.answer('Нельзя использовать кавычки! Введи без них')
        msg_id_write(msg, id)  # записывает айди сообщения в БД
    elif len(message.text) > 25:
        msg = await message.answer('Слишком длинно, не возьмусь')
        msg_id_write(msg, id)  # записывает айди сообщения в БД
    else:
        cur.execute("""INSERT INTO things VALUES(?,?)""", (id, message.text))  # добавление данных в список дел
        data_base.commit()  # подтверждение действий
        msg = await message.answer(f'Вот и добавили "{message.text}" в список дел', reply_markup=kb_start)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
        await message.delete()  # удалить сообщение пользователя


@dp.callback_query_handler()
async def del_thing(callback: types.CallbackQuery):
    id = callback.from_user.id  # посмотреть ID через коллбэки
    data_base = sq.connect('ListBotBase.db')  # связь с БД
    cur = data_base.cursor()
    cur.execute(f'DELETE FROM things WHERE thing = "{callback.data}" AND user_id = {id}')
    data_base.commit()
    await bot.delete_message(callback.from_user.id, callback.message.message_id)  # удаление предыдущего сообщения бота

    flag = check_data_base(id)
    if flag:
        list_kb = view_list(id)  # функция создает и возвращет список дел в виде клавиатуры
        await callback.answer('Дельце-то сделано!', show_alert=True)
        msg = await bot.send_message(callback.from_user.id, 'Актуальный список: ', reply_markup=list_kb)
        msg_id_write(msg, id)  # записывает айди сообщения в БД
    else:
        await callback.answer('Похоже, все дела переделаны. Мои поздравления!', show_alert=True)
        msg = await bot.send_message(callback.from_user.id, 'Продолжим?', reply_markup=kb_start)
        msg_id_write(msg, id)  # записывает айди сообщения в БД


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)  # skip_updates - бот не будет отвечать на сообщения, которые были присланы,
                                            # когда он был в офлайне
