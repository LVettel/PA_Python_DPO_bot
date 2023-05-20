from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from loguru import logger

API_token = '6158460170:AAFs9rB8NSyth1BuD6MjHmYboboiAa0uceI'
bot = Bot(token=API_token)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)

logger.add('logging.log', format="{time} {level} {message}", level="DEBUG")
