from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


API_token = '6269317196:AAFFnRmTIq3hHxR0te6CDHbyFQulVmQw8SE'
bot = Bot(token=API_token)
storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)