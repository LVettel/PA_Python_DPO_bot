from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


API_token = '6158460170:AAFs9rB8NSyth1BuD6MjHmYboboiAa0uceI'
bot = Bot(token=API_token)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)