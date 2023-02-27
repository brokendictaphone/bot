from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('создать список')
b2 = KeyboardButton('показать списки')
b3 = KeyboardButton('/help')
b4 = KeyboardButton('удалить список')
kb_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# клавиатура создается(кнопки будут изменяться под надписи, клавиатура будет удаляться после использования)
kb_start.add(b1, b2).row(b3, b4)  # добавление кнопок роу - ряд, адд - простое добавление

bt1 = KeyboardButton('выход из списка')
bt2 = KeyboardButton('удалить пункт из списка')
manage_list_kbrd = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
manage_list_kbrd.add(bt1).row(bt2)

btn1 = KeyboardButton('отмена')
cancel_del_kbrd = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
cancel_del_kbrd.add(btn1)



