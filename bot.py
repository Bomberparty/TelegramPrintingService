import asyncio
import logging
from loader import bot, dp
from handlers import userdialog, admindialog
from database import Database

logging.basicConfig(level=logging.INFO)


async def main():
    await bot.delete_webhook()
    dp.include_router(userdialog.router)
    dp.include_router(admindialog.router)
    await Database().init_database()
    await dp.start_polling(bot)
    await Database().close_database()

if __name__ == "__main__":
    asyncio.run(main())
