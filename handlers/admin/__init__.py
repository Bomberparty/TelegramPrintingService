from . import common
from . import printdialog

from aiogram.dispatcher.router import Router


router = Router()
router.include_routers(common.router, printdialog.router)

