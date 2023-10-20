from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.database.db import Database
from dotenv import load_dotenv
import logging
import os


load_dotenv()
bot = Bot(token=os.getenv('TOKEN_BOT'), parse_mode=types.ParseMode.HTML)#<- &lt; >- &gt; &- &amp;
logging.basicConfig(level=logging.INFO)
dp= Dispatcher(bot, storage=MemoryStorage())
db= Database(host=os.getenv('HOST_DB'),
             user=os.getenv('USER_DB'),
             password=os.getenv('PASSWORD_DB'),
             database=os.getenv('NAME_DB'),)