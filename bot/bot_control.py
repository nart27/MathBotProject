from contextlib import asynccontextmanager
from fastapi import FastAPI
import asyncio
from fastapi.responses import JSONResponse
from fastapi import status
import logging
from typing import AsyncIterator, Optional

logger = logging.getLogger(__name__)

class BotManager:
    def __init__(self):
        self.bot_task: Optional[asyncio.Task] = None
        self.shutdown_event = asyncio.Event()
        self.is_running: bool = False

    async def run_bot(self):
        self.is_running = True
        """Основная асинхронная задача бота"""
        from main import bot_main  # Ленивый импорт
        try:
            await bot_main(self.shutdown_event)
        except Exception as e:
            logger.error(f"Bot error: {e}")
        finally:
            self.is_running = False
            logger.info("Bot stopped")

bot_manager = BotManager()

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Управление жизненным циклом приложения"""
    # Запуск бота при старте
    bot_manager.bot_task = asyncio.create_task(bot_manager.run_bot())
    logger.info("Bot started automatically")
    
    yield
    
    # Остановка при завершении
    bot_manager.shutdown_event.set()
    if bot_manager.bot_task:
        await bot_manager.bot_task
    logger.info("Application shutdown complete")

app = FastAPI(lifespan=lifespan)


@app.post("/start")
async def start_bot():
    if bot_manager.bot_task and not bot_manager.bot_task.done():
        return JSONResponse(
            content={"detail": "Bot is already running"},
            # status_code=status.HTTP_409_CONFLICT
        )
    bot_manager.shutdown_event.clear()
    bot_manager.bot_task = asyncio.create_task(bot_manager.run_bot())
    return {"status": "started"}

@app.post("/stop")
async def stop_bot():
    if not bot_manager.bot_task or bot_manager.bot_task.done():
        return JSONResponse(
            content={"detail": "Bot is not running"},
            # status_code=status.HTTP_409_CONFLICT
        )
    bot_manager.shutdown_event.set()
    return {"status": "stopping"}


@app.post("/check")
async def get_status():
    return {
        "status": "running" if bot_manager.bot_task and not bot_manager.bot_task.done() else "stopped"
    }