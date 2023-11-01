from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def users_menu():
    markup= InlineKeyboardMarkup(row_width=1)

    markup.add(
        InlineKeyboardButton('Все пользователи', callback_data='allusers'),
        InlineKeyboardButton('Указать временной интервал', callback_data='span'),
    )

    return markup
