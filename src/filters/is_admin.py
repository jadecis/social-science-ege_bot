from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter
from config import ADMINS

# фильтр проверка на админа
class IsAdmin(BoundFilter):

    async def check(self, message: Message):
        return message.from_user.id in ADMINS