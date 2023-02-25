from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b1 = KeyboardButton('создать список')
b2 = KeyboardButton('показать списки')
b3 = KeyboardButton('/help')
b4 = KeyboardButton('удалить список')
kb_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# клавиатура создается(кнопки будут изменяться под надписи, клавиатура будет удаляться после использования)
kb_start.add(b1, b2).row(b3, b4)  # добавление кнопок роу - ряд, адд - простое добавление

bt1 = KeyboardButton('выход из списка')
exit_list_kbrd = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
exit_list_kbrd.add(bt1)