from aiogram.dispatcher.filters.state import StatesGroup, State

class Span(StatesGroup):
    tasks= State()
    users= State()