import datetime
import pprint
import requests
import json
from aiogram import types, Dispatcher
from project import search
from create_bot import dp

# search.register_message_handler(dp)

async def bothelp(message: types.Message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	button_1 = types.KeyboardButton(text='/lowprice')
	button_2 = types.KeyboardButton(text='/highprice')
	button_3 = types.KeyboardButton(text='/bestdeal')
	button_4 = types.KeyboardButton(text='/history')
	keyboard.add(button_1, button_2, button_3, button_4)
	await message.reply('Привет!\n'
						'Это бот турагенства To Easy Travel.\n'
						'С помощью этого бота вы можете получить следующую информацию:\n'
						'\t\t\t1. Узнать топ самых дешёвых отелей в городе (команда /lowprice).\n'
						'\t\t\t2. Узнать топ самых дорогих отелей в городе (команда /highprice).\n'
						'\t\t\t3. Узнать топ отелей, наиболее подходящих по цене и расположению от центра'
						'\t\t\t(самые дешёвые и находятся ближе всего к центру) (команда /bestdeal).\n'
						'\t\t\t4. Узнать историю поиска отелей (команда /history)', reply_markup=keyboard)


# async def low_price(message: types.Message):
# 	await message.reply('Эта команда для поиска самых дешёвых отелей в городе',
# 						reply_markup=types.ReplyKeyboardRemove())



# async def high_price(message: types.Message):
# 	await message.reply('Эта команда для поиска самых дорогих отелей в городе',
# 						reply_markup=types.ReplyKeyboardRemove())
#
#
# async def best_deal(message: types.Message):
# 	await message.reply('Эта команда для поиска наилучших предложений', reply_markup=types.ReplyKeyboardRemove())




async def history(message: types.Message):
	await message.reply('История поиска.', reply_markup=types.ReplyKeyboardRemove())

def register_handlers_main(dp: Dispatcher):
	dp.register_message_handler(callback=bothelp, commands=['start', 'help'])
	#
	# dp.register_message_handler(callback=low_price, commands=['highprice'])
	# dp.register_message_handler(callback=low_price, commands=['bestdeal'])
	dp.register_message_handler(callback=history, commands=['history'])
