from . import common
from . import printdialog
from . import scandialog

from aiogram.dispatcher.router import Router


router = Router()
router.include_routers(common.router, scandialog.router, printdialog.router)

# router.include_routers(scandialog.router)
