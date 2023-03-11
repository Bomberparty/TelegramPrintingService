import asyncio
import logging
import configparser
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser().read('config.ini')

bot = Bot(token=config['DEFAULT']['token'])

dp = Dispatcher()


