from aiogram.types import Message
from aiogram.dispatcher.filters import CommandStart
from loader import db, dp, bot 
from src.handlers.user.stats import get_stats
from src.keyboards.user.inline_markup import start_menu, type_decide, decide_tusk_but
from src.keyboards.admin.reply_markup import admin_menu
from aiogram.dispatcher import FSMContext
from datetime import date
from src.filters.is_admin import IsAdmin



@dp.message_handler(CommandStart(), state="*")
async def start_handler(msg: Message, state: FSMContext):
    await state.finish()
    db.add_user(
        {
                "user_id" : msg.from_user.id,
                "username" : msg.from_user.username,
                "full_name" : msg.from_user.full_name,
                "date_reg" : str(date.today())
        }
    )
    bot_info= await bot.get_me()
    await msg.answer(f"""
Привет! Я @{bot_info.username} - твой помощник при подготовке к ЕГЭ по обществознанию.

Я скидываю задачи из первой части ЕГЭ и проверяю твои ответы. Если ты не знаешь, как проверяются задания первой части и как их решать, то переходи в инстукцию

Начнем?""", reply_markup=start_menu())
    
@dp.message_handler(commands=['stats'], state="*")
async def stats_handler(msg: Message, state: FSMContext):
    await state.finish()
    message=get_stats(msg.chat.id)
    await msg.answer(message, reply_markup=decide_tusk_but('decide'))
    
@dp.message_handler(commands=['exercise'], state="*")
async def stats_handler(msg: Message, state: FSMContext):
    await state.finish()
    await msg.answer("Можем решать задачки рандомно по всем темам, а можем по отдельным разделам.   "
                              +"Что выбираешь?   P.S. Если не знаешь, как проверяются задания, или хочешь получить"
                              +"советы по решению, то жми инструкцию.", reply_markup=type_decide())
    
@dp.message_handler(IsAdmin(), commands=["admin"], state="*")
async def admin_com(msg: Message, state: FSMContext):
    await state.finish()
    await msg.answer("Меню", reply_markup=admin_menu())