import logging
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, BaseMiddleware
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import TelegramObject
from typing import Callable, Dict, Any, Awaitable

from config import config
from handlers import start, weather
from database.session import init_db, async_session

logging.basicConfig(level=logging.INFO)

# Middleware для автоматической передачи сессии БД в хэндлеры
class DbSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with async_session() as session:
            data["db_session"] = session
            return await handler(event, data)

async def main() -> None:
    # Инициализируем базу данных (создаем файлы и таблицы)
    await init_db()

    bot = Bot(
        token=config.telegram_token.get_secret_value(), 
        default_bot_properties=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    # Регистрируем middleware для БД
    dp.update.middleware(DbSessionMiddleware())

    dp.include_router(start.router)
    dp.include_router(weather.router)

    async with aiohttp.ClientSession() as client_session:
        await dp.start_polling(bot, client_session=client_session)

if __name__ == "__main__":
    asyncio.run(main())
