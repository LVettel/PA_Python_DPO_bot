from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
import search


class FSM_search(StatesGroup):
	city = State()
	rooms = State()
	in_date = State()
	out_date = State()
	photo = State()


@dp.message_handler(commands='lowprice', state=None)
async def start(message: types.Message):
	"""Начало составления конфигурации поиска по команде /lowprice"""

	await FSM_search.city.set()
	await message.reply('Это команда для поиска самых дешёвых отелей в городе.\n'
						'Введите город, в котором хотите остановиться.',
						reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=FSM_search.city)
async def city_name(message: types.Message, state: FSMContext):
	"""
	Принимается название искомого города и записывается в конфигурацию.
	Далее, идёт запрос на получение количества комнат в номере.
	"""

	async with state.proxy() as data:
		data['city_name'] = message.text
	await FSM_search.next()
	await message.answer('Введите количество комнат.')


@dp.message_handler(state=FSM_search.rooms)
async def rooms_set(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['rooms'] = message.text
	await FSM_search.next()
	await message.answer('Введите дату заселения.')


@dp.message_handler(state=FSM_search.in_date)
async def check_in_date(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['in_date'] = message.text
	await FSM_search.next()
	await message.answer('Введите дату уезда.')


@dp.message_handler(state=FSM_search.out_date)
async def check_out_date(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['out_date'] = message.text
	await FSM_search.next()
	await message.answer('Нужны ли Вам фотографии отеля?')


@dp.message_handler(state=FSM_search.photo)
async def hotel_photo(message: types.Message, state: FSMContext):
	async with state.proxy() as data:
		data['photo'] = message.text
	await message.answer('end')
	async  with state.proxy() as data:
		await message.answer(str(data))
	await state.finish()


def register_handlers_main(dp: Dispatcher):
	dp.register_message_handler(callback=start, commands=['lowprice'])
	dp.register_message_handler(callback=city_name, state=FSM_search.city)
	dp.register_message_handler(callback=rooms_set, state=FSM_search.rooms)
	dp.register_message_handler(callback=check_in_date, state=FSM_search.in_date)
	dp.register_message_handler(callback=check_out_date, state=FSM_search.out_date)
	dp.register_message_handler(callback=hotel_photo, state=FSM_search.photo)
