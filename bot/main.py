import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from bot import config
from bot.handlers import router
from bot.services.logger import logger


async def main() -> None:
    if config.BOT_TOKEN is None:
        raise ValueError("BOT_TOKEN is not set in .env")

    logger.info("Starting bot initialization...")

    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)

    await bot.set_my_commands([BotCommand(command="/start", description="Начать чат")])

    logger.info("🤖 Bot is running and polling!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
