import logging
from typing import Self, Tuple

from aiogram import Router, Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot_models.connect import Connect


class BotBuilder:
    _db_connection: Connect = Connect
    _router: Tuple[Router, ...] = []
    _token: str

    def set_token(self, token: str) -> Self:
        self._token = token
        return self

    def set_routers(self, *router: Router) -> Self:
        self._router = router
        return Self

    def set_db_connection(self, connection: Connect) -> Self:
        self._db_connection = connection
        return self

    async def run(self) -> None:
        bot = Bot(self._token)
        storage_bot = MemoryStorage()
        logging.log(logging.INFO, await bot.get_me())
        dp = Dispatcher(storage=storage_bot)
        dp.include_routers(*self._router)
        await dp.start_polling(bot)
