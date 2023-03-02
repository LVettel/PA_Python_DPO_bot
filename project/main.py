def low_price():
	return 'Эта команда для поиска самых дешёвых отелей в городе'


def high_price():
	return 'Эта команда для поиска самых дорогих отелей в городе'


def best_deal():
	return 'Эта команда для поиска наилучших предложений'


def history():
	return 'История поиска'


import requests

url = "https://hotels4.p.rapidapi.com/v2/get-meta-data"

headers = {
	"X-RapidAPI-Key": "0112463613mshae3918b4653745dp16544ejsnfb6a9f2d2dbd",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

print(response.text)