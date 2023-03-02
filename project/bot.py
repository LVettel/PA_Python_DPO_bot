from aiogram import Bot, Dispatcher, executor, types
import main

API_token = '6269317196:AAFFnRmTIq3hHxR0te6CDHbyFQulVmQw8SE'
bot = Bot(token=API_token)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
	keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
	button_1 = types.KeyboardButton(text='/help')
	keyboard.add(button_1)
	await message.reply('Привет!\nЭто бот для турагенства To Easy Travel.', reply_markup=keyboard)


@dp.message_handler(commands=['lowprice'])
async def test1(message: types.Message):
	await message.reply(main.low_price(), reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['highprice'])
async def test1(message: types.Message):
	await message.reply(main.high_price(), reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['bestdeal'])
async def test1(message: types.Message):
	await message.reply(main.best_deal(), reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['history'])
async def test1(message: types.Message):
	await message.reply(main.history(), reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands=['help'])
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


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=False)
