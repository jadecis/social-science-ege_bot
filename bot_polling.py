from loader import dp
from aiogram import executor
from aiogram.types import BotCommand
from src.commands import main_commands
from src.handlers.user import main_handlers, tasks

async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        BotCommand("start", "Перезапуск бота"),
        BotCommand("exercise", "Порешать задачки"),
        BotCommand("about", "Что может бот"),
        BotCommand("stats", "Показать мои успехи"),
    ])

async def startup(dp):
    await set_default_commands(dp)
    # asyncio.create_task(scheduler())
    
executor.start_polling(dp, skip_updates=False, on_startup=startup)