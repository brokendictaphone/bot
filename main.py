from aiogram.utils import executor
from aiogram import types
from keyboard import kb_start
from create_bot import dp
from funct import *
from handlers import AddListsHandlers, DelListHandlers, ViewListHandlers, ViewItemHandlers, AddItemHandlers, DelItemsHandlers


data_base = sq.connect('ListBotBase2.db')
cur = data_base.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS lists (
    user_id INT,
    list NULL,
    thing TXT
)""")   # создание таблицы в базе данных если она ещё не создана, в скобках указаны столбцы и тип данных в них

cur.execute("""CREATE TABLE IF NOT EXISTS msg_ids (
    user_id INT,
    msg NULL
)""")   # создание таблицы с мессадж айди, в скобках указаны столбцы и тип данных в них

cur.execute("""CREATE TABLE IF NOT EXISTS current_list (
    user_id INT,
    list_name TXT
)""")   # создание таблицы

data_base.commit()  # подтверждение действий
data_base.close()  # закрытие ДБ


async def on_startup(_):  # служебное сообщение
    print('всё отлично: бот онлайн')


@dp.message_handler(commands=['start', 'help'])  # команда старт и кнопки
async def command_start(message: types.Message):
    id = message.chat.id
    await del_mess(id)  # удаление предыдущего сообщения
    msg = await bot.send_message(message.from_user.id, f'Привет, {message.chat.first_name.title()}!'
                                                 f' Я бот для составления списков, для того чтобы добавить что-нибудь'
                                                 f' в список, просто отправь это мне.'
                                                 f' Чтобы удалить что-то из списка, нажми на кнопку с названием этого что-то.'
                                                 f' Пожалуй, это всё, что нужно знать о моей работе))', reply_markup=kb_start)
    msg_id_write(msg, id)  # записывает айди сообщения в БД
    await message.delete()  # удалить сообщение пользователя

ViewListHandlers.register_view_list_handlers(dp)  # просмотр пользовательских списков
DelListHandlers.register_del_list_handlers(dp)  # удаление пользовательских списков
AddListsHandlers.register_AddLIst_handlers(dp)  # добавление пользовательских списков
ViewItemHandlers.register_view_item_handlers(dp)  # просмотр пунктов в ПС
AddItemHandlers.register_add_item_handlers(dp)  # добавление пунктов в ПС
DelItemsHandlers.register_del_item_handlers(dp)  # удаление пунктов в ПС


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)  # skip_updates - бот не будет отвечать на сообщения, которые были присланы,
                                            # когда он был офлайн
