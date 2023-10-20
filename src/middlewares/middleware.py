from aiogram import Dispatcher
from loader import db
from aiogram.dispatcher.handler import CancelHandler  # отменяет вызов хэндлера
from aiogram.dispatcher.middlewares import BaseMiddleware  # класс Middleware от Aiogram
from aiogram.types import Message, CallbackQuery, InlineQuery

class UserBannedMiddleware(BaseMiddleware):
    async def on_process_message(self, message: Message, data: dict):
        db.add_user(
            {
                "user_id" : message.from_user.id,
                "username" : message.from_user.username,
                "full_name" : message.from_user.full_name,
            }
        )
        # if db.check_user(message.from_user.id):
        #     await message.answer(
        #         '<b> Ваш аккаунт заблокирован!</b>'
        #     )
        #     raise CancelHandler()

    # async def on_process_callback_query(self, call: CallbackQuery, data: dict):
    #     if db.check_user(call.from_user.id):
    #         await call.answer(
    #             ' Ваш аккаунт заблокирован!',
    #             show_alert=True
    #         )
    #         raise CancelHandler()

    # async def on_process_inline_query(self, query: InlineQuery, data: dict):
    #     if db.check_user(query.from_user.id):
    #         raise CancelHandler()
        