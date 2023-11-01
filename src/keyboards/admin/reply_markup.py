from aiogram.types import ReplyKeyboardMarkup

def admin_menu():
    markup= ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    markup.add(
        'Пользователи',
        'Статистика решений'
    )

    return markup