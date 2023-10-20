from aiogram.dispatcher.filters.state import StatesGroup, State

class Task(StatesGroup):
    answer= State()
    decide= State()