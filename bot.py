import asyncio
import logging
from loader import bot, dp, dbname
from handlers import userdialog, admindialog
from database import Database
from migrations.run import run_migrations

logging.basicConfig(level=logging.INFO)


async def main():
    run_migrations(dbname=dbname)
    await bot.delete_webhook()
    dp.include_router(userdialog.router)
    dp.include_router(admindialog.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
