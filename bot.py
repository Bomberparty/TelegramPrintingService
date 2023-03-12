import asyncio
import logging
from loader import bot, dp
from handlers import common


logging.basicConfig(level=logging.INFO)


async def main():
    await bot.delete_webhook()
    dp.include_router(common.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
