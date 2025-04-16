import asyncio
from aiogram import Router, F, Bot, Dispatcher
from aiogram.types import Message
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

async def bot_main(shutdown_event: asyncio.Event):
    """Основная логика бота"""
    bot = Bot(token="API-TOKEN")
    dp = Dispatcher()
    router = Router()  # создаётся при каждом запуске

    def register_handlers():
        @router.message(F.text == "/start")
        async def start_handler(message: Message):
            await message.answer("Бот работает!")

        @router.message(F.text == "/open_day")
        async def open_day_handler(message: Message):
            await message.answer(
                "📅 День открытых дверей:\n\n"
                "Дата: 15 сентября 2024\n"
                "Место: Матфак, ауд. 301\n"
                "Программа:\n"
                "10:00 - Презентация программ\n"
                "12:00 - Мастер-классы"
            )

    register_handlers()
    dp.include_router(router)

    polling_task = asyncio.create_task(dp.start_polling(bot))

    async def shutdown_watcher():
        await shutdown_event.wait()
        logger.info("Shutdown signal received")
        await dp.stop_polling()

    await asyncio.gather(polling_task, shutdown_watcher())
    await bot.session.close()
    logger.info("Bot shutdown complete")

if __name__ == "__main__":
    async def run():
        shutdown_event = asyncio.Event()
        try:
            await bot_main(shutdown_event)
        except KeyboardInterrupt:
            shutdown_event.set()
    
    asyncio.run(run())