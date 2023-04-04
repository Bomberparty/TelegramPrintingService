import configparser
from aiogram import Bot, Dispatcher

config = configparser.ConfigParser()

config.read("settings.ini")

admins = config["DEFAULT"]["admins"].split()

dbname = config["DEFAULT"]["dbname"].split()[0]

bot = Bot(token=config['DEFAULT']['token'])

dp = Dispatcher()
