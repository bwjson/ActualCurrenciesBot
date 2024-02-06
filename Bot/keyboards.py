from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

b1 = KeyboardButton('/help')
b2 = KeyboardButton('/price')
b3 = KeyboardButton('/convert')
b4 = KeyboardButton('/news')
kb = ReplyKeyboardMarkup(resize_keyboard=True)
kb.add(b1).add(b2).add(b3).add(b4)

start_kb = InlineKeyboardMarkup()
start_b = InlineKeyboardButton("Start", callback_data='start_bot')
start_kb.add(start_b)