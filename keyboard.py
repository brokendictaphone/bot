from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

b2 = KeyboardButton('показать список')
b3 = KeyboardButton('/help')
kb_start = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# клавиатура создается(кнопки будут изменяться под надписи, клавиатура будет удаляться после использования)
kb_start.add(b2).row(b3)  # добавление кнопок роу - ряд, адд - простое добавление
