
from aiogram import types, Dispatcher
from project.create_bot import dp, bot
import requests



# @dp. message_handler(state=None)
# async def set_city(message: types.Message):
# 	await FSM_search.city.set()
# 	await message.answer('Введите город')
#
#
#
# @dp. message_handler(state=FSM_search.city)
# async def set_rooms(message: types.Message):
# 	await FSM_search.next()
# 	await message.answer('Введите количество комнат')


# def register_message_handler(dp: Dispatcher):
# 	dp.register_message_handler(set_city)
# 	dp.register_message_handler(set_rooms)


def city_search():
	url = "https://hotels4.p.rapidapi.com/locations/v3/search"

	querystring = {"q": "Рига", "locale": "en_US", "langid": "1033", "siteid": "300000001"}

	headers = {
		"X-RapidAPI-Key": "14cb351c01msh1c48214e3041834p18ae28jsndbaf16e16c16",
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)

def hotel_search():
	url = "https://hotels4.p.rapidapi.com/properties/v2/list"

	headers = {
		"X-RapidAPI-Key": "14cb351c01msh1c48214e3041834p18ae28jsndbaf16e16c16",
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}
	payload = {
		"currency": "USD",
		"eapid": 1,
		"locale": "en_US",
		"siteId": 300000001,
		"destination": {"regionId": "3000"},
		"checkInDate": {
			"day": 10,
			"month": 10,
			"year": 2023
		},
		"checkOutDate": {
			"day": 15,
			"month": 10,
			"year": 2023
		},
		"rooms": [
			{"adults": 1}
		],
		"resultsStartingIndex": 0,
		"resultsSize": 200,
		"sort": "PRICE_LOW_TO_HIGH",
		"filters": {"price": {
			"max": 150,
			"min": 100
		}}
	}

	response = requests.request("POST", url, json=payload, headers=headers)