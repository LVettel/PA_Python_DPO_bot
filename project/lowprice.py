from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp
import search
sort = []

class FSM_search(StatesGroup):
	city = State()
	rooms = State()
	in_date = State()
	out_date = State()
	photo = State()


async def start_lowprice(message: types.Message):
	"""
	Начало составления конфигурации поиска по команде /lowprice и /bestdeal
	"""
	# sort[0] = 'PRICE_LOW_TO_HIGH'
	await FSM_search.city.set()
	await message.reply('Это команда для поиска самых дешёвых отелей в городе.\n'
						'Введите город, в котором хотите остановиться.',
						reply_markup=types.ReplyKeyboardRemove())


async def start_highprice(message: types.Message):
	"""
	Начало составления конфигурации поиска по команде /highprice
	"""
	# sort[0] = 'PRICE_HIGH_TO_LOW'
	await FSM_search.city.set()
	await message.reply('Это команда для поиска самых дешёвых отелей в городе.\n'
						'Введите город, в котором хотите остановиться.',
						reply_markup=types.ReplyKeyboardRemove())


async def city_name(message: types.Message, state: FSMContext):
	"""
	Принимается название искомого города и записывается в конфигурацию.
	Исполняется функция city_search из модуля search.
	Далее, идёт запрос на получение количества комнат в номере.
	"""

	async with state.proxy() as data:
		data['city_id'] = search.city_search(name= message.text)
		if data['city_id'] is not 'none':
			await FSM_search.next()
			await message.answer('Введите количество комнат.')
		else:
			await state.finish()
			await message.reply('Такого города нет в нашем каталоге')



async def rooms_set(message: types.Message, state: FSMContext):
	"""
	Принимается количество комнат в номере и записывается в конфигурацию.
	Далее идёт запрос на получение даты заселения.
	:param message:
	:param state:
	:return:
	"""
	async with state.proxy() as data:
		data['rooms'] = int(message.text)
	await FSM_search.next()
	await message.answer('Введите дату заселения в формате - День.Месяц.Год.')


async def check_in_date(message: types.Message, state: FSMContext):
	"""
	Принимается дата заселения в отель и записывается в конфигурацию.
	Далее идёт запрос на получение даты уезда.
	:param message:
	:param state:
	:return:
	"""
	async with state.proxy() as data:
		data['in_date'] = message.text.split('.')
	await FSM_search.next()
	await message.answer('Введите дату уезда в формате - День.Месяц.Год.')


async def check_out_date(message: types.Message, state: FSMContext):
	"""
	Принимается дата уезда из отеля и записывается в конфигурацию.
	Далее идёт запрос на получение надобности фотографий.
	:param message:
	:param state:
	:return:
	"""
	async with state.proxy() as data:
		data['out_date'] = message.text.split('.')
	await FSM_search.next()
	await message.answer('Нужны ли Вам фотографии отеля? Да/Нет')


async def hotel_photo(message: types.Message, state: FSMContext):
	"""
	Принимается надобность фотографий пользователю и записывается в конфигурацию.
	Далее идёт исполнение функции hotel_search из модуля search.
	:param message:
	:param state:
	:return:
	"""
	async with state.proxy() as data:
		data['photo'] = message.text
	await message.answer('end')
	async with state.proxy() as data:
		await message.answer(str(data))
	search.hotel_search(
		id=data['city_id'],
		rooms=data['rooms'],
		in_date=data['in_date'],
		out_date=data['out_date'],
		sort=sort[0]
						)
	await state.finish()


async def reset_state(message: types.Message, state: FSMContext):
	"""
	Функция отмены любого состояния машины состояний.
	:param message:
	:param state:
	:return:
	"""
	current_state = await state.get_state()
	if current_state is None:
		return
	await state.reset_state()
	await message.reply('Отмена составления конфигурации поиска')


def register_handlers_lowprice(dp: Dispatcher):
	"""
	Функция регистрации хендлеров модуля в боте.
	:param dp:
	:return:
	"""
	dp.register_message_handler(callback=start_lowprice, commands=['lowprice', '/bestdeal'])
	dp.register_message_handler(callback=start_highprice, commands=['/highprice'])
	dp.register_message_handler(callback=city_name, state=FSM_search.city)
	dp.register_message_handler(callback=rooms_set, state=FSM_search.rooms)
	dp.register_message_handler(callback=check_in_date, state=FSM_search.in_date)
	dp.register_message_handler(callback=check_out_date, state=FSM_search.out_date)
	dp.register_message_handler(callback=hotel_photo, state=FSM_search.photo)
	dp.register_message_handler(callback=reset_state,
								state=[
									FSM_search.city,
									FSM_search.rooms,
									FSM_search.in_date,
									FSM_search.out_date,
									FSM_search.photo
								],
								commands=['cancel'])

