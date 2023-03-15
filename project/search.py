from aiogram import types, Dispatcher
from project.create_bot import dp, bot
import requests
import json


def city_search(name) -> str:
	"""
	Функция поиска нужного города.
	Возвращает id города.
	:param name:
	:return:
	"""
	url = "https://hotels4.p.rapidapi.com/locations/v3/search"

	querystring = {"q": "{}".format(name), "locale": "ru_RU", "langid": "1033", "siteid": "300000001"}

	headers = {
		"X-RapidAPI-Key": "14cb351c01msh1c48214e3041834p18ae28jsndbaf16e16c16",
		"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	data = json.loads(response.text)
	# hotel_search(id=data['sr'][0]['gaiaId'])
	return data['sr'][0]['gaiaId']


def hotel_search(id: str, rooms: int, in_date: list, out_date: list, sort: str):
	"""
	Функция поиска отелей в найденном городе.
	Возвращает список отсортированных по цене отелей.
	:param id:
	:param rooms: int
	:param in_date: list(str)
	:param out_date: list(str)
	:param sort: str
	:return:
	"""
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
		"destination": {"regionId": "{}".format(id)},
		"checkInDate": {
			"day": int(in_date[0]),
			"month": int(in_date[1]),
			"year": int(in_date[2])
		},
		"checkOutDate": {
			"day": int(out_date[0]),
			"month": int(out_date[1]),
			"year": int(out_date[2])
		},
		"rooms": [
			{"adults": int(rooms)}
		],
		"resultsStartingIndex": 0,
		"resultsSize": 200,
		"sort": "{}".format(sort),
		"filters": {"price": {
			"max": 150,
			"min": 100
		}}
	}

	response = requests.request("POST", url, json=payload, headers=headers)
