import configparser
from aiogram import Bot, Dispatcher

config = configparser.ConfigParser()

config.read("settings.ini")

admins = list(map(int, config["ADMINS"]["admin_id"].split()))

admin_nspk_number = list(map(int, config["ADMINS"]["admin_nspk_number"].split()))

bot = Bot(token=config['DEFAULT']['token'])

dp = Dispatcher()
