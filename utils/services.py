import asyncio
import datetime
import os
import database

import aioschedule


async def cancel_old_tasks():
    id_list = await database.Database().get_confirming_task_list()
    directory = "media/"
    for task_id in id_list:
        file_path = os.path.join(directory, f"{task_id[0]}.pdf")
        a = os.path.getmtime(file_path)
        time = (datetime.datetime.utcnow() -
                datetime.datetime.utcfromtimestamp(a)).seconds
        if time > 24 * 60 * 60:
            await database.Database().\
                update_task_status(database.TaskStatus.CANCELED)


async def register_services():
    aioschedule.every(12).hours.do(cancel_old_tasks)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(60 * 60 * 5)


async def main():
    await delete_old_files()


if __name__ == "__main__":
    asyncio.run(main())
