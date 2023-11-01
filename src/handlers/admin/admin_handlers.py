from aiogram.types import Message, CallbackQuery
from loader import db, dp
from src.keyboards.admin.reply_markup import admin_menu
from src.keyboards.admin.inline_markups import *
from src.states.admin.state import Span
from aiogram.dispatcher import FSMContext
from datetime import datetime, date
import csv
import os

@dp.message_handler(text="Пользователи", state="*")
async def users_hand(msg: Message, state: FSMContext):
    await state.finish()
    await msg.answer("Выбери дальнейше действие:", reply_markup= users_menu())

@dp.message_handler(text="Статистика решений", state="*")
async def users_hand(msg: Message, state: FSMContext):
    await state.finish()
    await msg.answer("Отправь промежуток по форме дд.мм.гггг - дд.мм.гггг\n"
                     +"Например: 20.10.2023 - 28.10.2023")
    await Span.tasks.set()
    
@dp.message_handler(content_types=['text'], state= Span.tasks)
async def span_task_hand(msg: Message, state: FSMContext):
    dates= msg.text.split('-') #or msg.text.split('-')    
    dtbeg= datetime.strptime(dates[0].strip(), "%d.%m.%Y").strftime("%Y-%m-%d %H:%M:%S")
    dtend= datetime.strptime(dates[1].strip(), "%d.%m.%Y").strftime("%Y-%m-%d %H:%M:%S")
    await msg.answer(f"Количество решеных заданий за <i>{msg.text}</i>: <b>{db.get_stats_decide(dtbeg, dtend)}</b> шт")
    await state.finish()

@dp.callback_query_handler(text='allusers')
async def allusers_hand(call: CallbackQuery, state: FSMContext):
    users= db.get_stats_user()
    with open('src/handlers/admin/tables/users.csv', 'w+', newline="", encoding="utf-8-sig") as file:
        writer= csv.writer(file, delimiter=';')
        writer.writerow(
            ('user_id', 'username', 'fullname', 'date_reg')
        )
        for i in users:
            writer.writerow(
                (i.get('user_id'), i.get('username'), i.get('fullname'), i.get('date_reg'), )
            )
    await call.message.answer_document(document= open(f'src/handlers/admin/tables/users.csv', 'rb'))
    os.remove('src/handlers/admin/tables/users.csv')

@dp.callback_query_handler(text='span')
async def allusers_hand(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Отправь промежуток по форме дд.мм.гггг - дд.мм.гггг\n"
                +"Например: 20.10.2023 - 28.10.2023")
    await Span.users.set()

@dp.message_handler(content_types=['text'], state= Span.users)
async def span_task_hand(msg: Message, state: FSMContext):
    dates= msg.text.split('-') #or msg.text.split('-')    
    dtbeg= datetime.strptime(dates[0].strip(), "%d.%m.%Y").date().strftime("%Y.%m.%d")
    dtend= datetime.strptime(dates[1].strip(), "%d.%m.%Y").date().strftime("%Y.%m.%d")
    users= db.get_stats_user(dtbeg, dtend)
    with open('src/handlers/admin/tables/users.csv', 'w+', newline="", encoding="utf-8-sig") as file:
        writer= csv.writer(file, delimiter=';')
        writer.writerow(
            ('user_id', 'username', 'fullname', 'date_reg')
        )
        for i in users:
            writer.writerow(
                (i.get('user_id'), i.get('username'), i.get('fullname'), i.get('date_reg'), )
            )
    await msg.answer_document(document= open(f'src/handlers/admin/tables/users.csv', 'rb'))
    os.remove('src/handlers/admin/tables/users.csv')