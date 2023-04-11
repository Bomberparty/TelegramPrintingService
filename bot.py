import asyncio
import logging
from loader import bot, dp
from handlers import userdialog, admindialog
from utils.services import register_services
from migrations.run import run_migrations

logging.basicConfig(level=logging.INFO)


async def main():
    run_migrations()
    await bot.delete_webhook()
    dp.include_router(admindialog.router)
    dp.include_router(userdialog.router)
    asyncio.create_task(register_services())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
