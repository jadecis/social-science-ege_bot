from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def start_menu():
    markup= InlineKeyboardMarkup(row_width=1)
    
    markup.add(
        InlineKeyboardButton('Решать задачи', callback_data='decide'),
        # InlineKeyboardButton('Инструкция', callback_data='instruction'),
        # InlineKeyboardButton('Посмотреть статистику', callback_data='stat'),
    )
    
    return markup

def decide_tusk_but(callback):
    markup= InlineKeyboardMarkup(row_width=1)
    
    markup.add(
        InlineKeyboardButton('Решать задачи', callback_data=callback),
    )
    return markup

def task_menu(decide=True):
    markup= InlineKeyboardMarkup(row_width=1)
    if decide:
        markup.add(
            InlineKeyboardButton('Не знаю, показать решение', callback_data='taskDecide'),
        )
    markup.add(
        InlineKeyboardButton('Следующая задача', callback_data='nextTask'),
    )
    
    return markup

def answer_menu(answer=True):
    markup= InlineKeyboardMarkup(row_width=1)
    if answer:
        markup.add(
            InlineKeyboardButton('Показать решение', callback_data='showDecide'),
        )
    markup.add(
        InlineKeyboardButton('Следующая задача', callback_data='nextTaskdelete'),
    )
    
    return markup

def back_task():
    markup= InlineKeyboardMarkup(row_width=1)
    
    markup.add(
        InlineKeyboardButton('Вернуться к заданию', callback_data='returnTask'),
    )
    
    return markup

def type_decide():
    markup= InlineKeyboardMarkup(row_width=3)
    
    markup.add(
        InlineKeyboardButton('Рандомно', callback_data='random'),
        InlineKeyboardButton('По разделам', callback_data='section'),
        InlineKeyboardButton('Инструкция', callback_data='instruction'),
    )
    
    return markup

def section_menu():
    markup= InlineKeyboardMarkup(row_width=1)
    
    markup.add(
        InlineKeyboardButton('Человек и общество', callback_data='section_4'),
        InlineKeyboardButton('Экономика', callback_data='section_5'),
        InlineKeyboardButton('Социология', callback_data='section_3'),
        InlineKeyboardButton('Политика', callback_data='section_1'),
        InlineKeyboardButton('Право', callback_data='section_2'),
    )
    
    return markup