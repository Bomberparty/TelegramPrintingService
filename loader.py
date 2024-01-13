import configparser
from aiogram import Bot, Dispatcher

config = configparser.ConfigParser()

config.read("settings.ini")

admins = list(map(int, config["ADMINS"]["admin_id"].split()))

admin_nspk_number = list(map(int, config["ADMINS"]["admin_nspk_number"].split()))

yoomoney_enable = config["YOOMONEY"]["enable"] == "True"
yoomoney_token = config["YOOMONEY"]["token"] if yoomoney_enable else ""

bot = Bot(token=config["DEFAULT"]["token"])
scanner = config["DEFAULT"]["scanner"]
dp = Dispatcher()
