from aiogram.dispatcher import FSMContext
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
import search
import history


class FSM_search(StatesGroup):
	city = State()
	max_price = State()
	rooms = State()
	in_date = State()
	out_date = State()
	count = State()
	photo = State()


async def start_lowprice(message: types.Message, state: FSMContext):
	"""
	Начало составления конфигурации поиска по команде /lowprice
	"""
	await FSM_search.city.set()
	async with state.proxy() as data:
		data['user_id'] = message.from_user.id
		data['command'] = 'lowprice'
		data['sort'] = 'PRICE_LOW_TO_HIGH'
		data['bestdeal'] = False
		data['max_price'] = 100
	await message.reply('Это команда для поиска самых дешёвых отелей в городе.\n'
						'Введите город, в котором хотите остановиться.',
						reply_markup=types.ReplyKeyboardRemove())


async def start_highprice(message: types.Message, state: FSMContext):
	"""
	Начало составления конфигурации поиска по команде /highprice
	"""
	await FSM_search.city.set()
	async with state.proxy() as data:
		data['user_id'] = message.from_user.id
		data['command'] = 'highprice'
		data['sort'] = 'PRICE_HIGH_TO_LOW'
		data['bestdeal'] = False
		data['max_price'] = 1000
	await message.reply('Это команда для поиска самых дорогих отелей в городе.\n'
						'Введите город, в котором хотите остановиться.',
						reply_markup=types.ReplyKeyboardRemove())


async def start_bestdeal(message: types.Message, state: FSMContext):
	"""
	Начало составления конфигурации поиска по команде /bestdeal
	"""
	await FSM_search.city.set()
	async with state.proxy() as data:
		data['user_id'] = message.from_user.id
		data['command'] = 'bestdeal'
		data['sort'] = 'DISTANCE'
		data['bestdeal'] = True
	await message.reply('Это команда для поиска самых удобных отелей в городе.\n'
						'Введите город, в котором хотите остановиться.',
						reply_markup=types.ReplyKeyboardRemove())



async def city_name(message: types.Message, state: FSMContext):
	"""
	Принимается название искомого города и записывается в конфигурацию.
	Исполняется функция city_search из модуля search.
	Далее, идёт запрос на получение количества комнат в номере.
	"""

	async with state.proxy() as data:
		data['city_name'] = message.text
		data['city_id'] = search.city_search(name=message.text)

		if data['bestdeal']:
			if data['city_id'] != 'none':
				await FSM_search.next()
				await message.answer('Введите максимальную ожидаемую цену в $.')

			else:
				await state.finish()
				await message.reply('Такого города нет в нашем каталоге')

		else:
			if data['city_id'] != 'none':
				await FSM_search.rooms.set()
				await message.answer('Введите количество комнат.')

			else:
				await state.finish()
				await message.reply('Такого города нет в нашем каталоге')

async def max_price(message:types.Message, state: FSMContext):
	"""
	Функция для команды /bestdeal. Принимает в себя максимальную ожидаемую цену у пользователя
	и далее запрашивает количество комнат
	:param message:
	:param state:
	:return:
	"""
	async with state.proxy() as data:
		data['max_price'] = int(message.text)

	await FSM_search.next()
	await message.answer('Введите количество комнат.')


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
	Далее идёт запрос на нужное количество отелей в ответе.
	:param message:
	:param state:
	:return:
	"""
	async with state.proxy() as data:
		data['out_date'] = message.text.split('.')

	await FSM_search.next()
	await message.answer('Сколько вам нужно отелей в ответе?\n')



async def search_count(message: types.Message, state: FSMContext):
	"""
	Принимается число, количество отелей в ответе.
	Далее идёт запрос на получение надобности и количества(если нужно) фотографий.
	:param message:
	:param state:
	:return:
	"""
	async with state.proxy() as data:
		data['hotel_count'] = int(message.text)

	await FSM_search.next()
	await message.answer('Нужны ли Вам фотографии отеля? Да 3(количество фотографий)/Нет.\n')

async def hotel_photo(message: types.Message, state: FSMContext):
	"""
	Принимается надобность фотографий пользователю и записывается в конфигурацию.
	Далее идёт исполнение функции hotel_search из модуля search.
	:param message:
	:param state:
	:return:
	"""
	async with state.proxy() as data:
		data['photo'] = message.text.split(' ')
		print(data)
		history.config_create(data=data)
	await message.answer('Ведётся поиск...')



	hotel_list = search.hotel_search(
		id=data['city_id'],
		rooms=data['rooms'],
		in_date=data['in_date'],
		out_date=data['out_date'],
		sort=data['sort'],
		hotel_count=data['hotel_count'],
		photo=data['photo'],
		best_deal=data['bestdeal'],
		max_price=data['max_price']
						)

	for hotel, desc in hotel_list[0].items():
		answer = 'Название отеля: {name}.\n' \
				 'Минимальная цена: {price}.\n' \
				 'Адрес: {address}.\n'.format(name=hotel,
											price=desc['min_price'],
											address=desc['address'],
											)

		await message.answer(answer)

		photo_group = []
		for photo in desc['photo']:
			photo_group.append(photo)

		history.results_create(data=hotel_list, photo_group=photo_group)

		await message.answer_media_group(photo_group)
		if data['bestdeal']:
			distance = 'Расстояние до центра: {dist} км.'.format(dist=desc['distance'])
			await message.answer(distance)

	# await message.answer(hotel_list)
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
	await message.reply('Отмена составления конфигурации поиска')
	await state.finish()



def register_handlers_lowprice(dp: Dispatcher):
	"""
	Функция регистрации хендлеров модуля в боте.
	:param dp:
	:return:
	"""
	dp.register_message_handler(callback=start_lowprice, commands=['lowprice'])
	dp.register_message_handler(callback=start_highprice, commands=['highprice'])
	dp.register_message_handler(callback=start_bestdeal, commands=['bestdeal'])
	dp.register_message_handler(callback=city_name, state=FSM_search.city)
	dp.register_message_handler(callback=max_price, state=FSM_search.max_price)
	dp.register_message_handler(callback=rooms_set, state=FSM_search.rooms)
	dp.register_message_handler(callback=check_in_date, state=FSM_search.in_date)
	dp.register_message_handler(callback=check_out_date, state=FSM_search.out_date)
	dp.register_message_handler(callback=search_count, state=FSM_search.count)
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

