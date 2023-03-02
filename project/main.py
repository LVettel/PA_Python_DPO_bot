import datetime
import pprint

def low_price():
	return 'Эта команда для поиска самых дешёвых отелей в городе'


def high_price():
	return 'Эта команда для поиска самых дорогих отелей в городе'


def best_deal():
	return 'Эта команда для поиска наилучших предложений'


def history():
	return 'История поиска'


import requests

url = "https://hotels4.p.rapidapi.com/locations/v3/search"

headers = {
	"X-RapidAPI-Key": "0112463613mshae3918b4653745dp16544ejsnfb6a9f2d2dbd",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

params = {'q': 'Рига', 'locate': 'ru_RU'}
response = requests.request("GET", url, headers=headers, params=params)

pprint.pprint(response.text)

url2 = 'https://hotels4.p.rapidapi.com/properties/v2/list'

payload = {'currency': 'USD',
           'eapid': 1,
           'locale': 'ru_RU',
           'siteId': 300000001,
           'destination': '3000', # id из первого запроса,
           'checkInDate': {'day': 3, 'month': 3, 'year': 2023},
           'checkOutDate': {'day': 6, 'month': 3, 'year': 2023},
           'rooms': [{'adults': 1}],
           'resultsStartingIndex': 0,
           'resultsSize': 10,
           'sort': 'PRICE_LOW_TO_HIGH',
           'filters': {'availableFilter': 'SHOW_AVAILABLE_ONLY'}
           }

response = requests.request('POST', url=url2, headers=headers, params=payload)
pprint.pprint(response.text)