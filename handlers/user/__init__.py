from aiogram.dispatcher.router import Router

from . import common, printdialog, scandialog


router = Router()
router.include_routers(common.router, printdialog.router, scandialog.router)
