import json
import pprint
import requests



# def city_search():
#     url = "https://hotels4.p.rapidapi.com/locations/v3/search"
#
#     querystring = {"q":"Рига","locale":"en_US","langid":"1033","siteid":"300000001"}
#
#     headers = {
#        "X-RapidAPI-Key": "14cb351c01msh1c48214e3041834p18ae28jsndbaf16e16c16",
#        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
#     }
#
#     response = requests.request("GET", url, headers=headers, params=querystring)
#
#     pprint.pprint(response.text)
#
#     print('\n\n\n\n\n\n')
#
#
#
# def hotel_search():
#     url2 = "https://hotels4.p.rapidapi.com/properties/v2/list"
#
#     payload = {
#        "currency": "USD",
#        "eapid": 1,
#        "locale": "en_US",
#        "siteId": 300000001,
#        "destination": {"regionId": "3000"},
#        "checkInDate": {
#                                      "day": 10,
#                                      "month": 10,
#                                      "year": 2023
#        },
#        "checkOutDate": {
#                                       "day": 15,
#                                      "month": 10,
#                                      "year": 2023
#        },
#        "rooms": [
#           {"adults": 1}
#        ],
#        "resultsStartingIndex": 0,
#        "resultsSize": 200,
#        "sort": "PRICE_LOW_TO_HIGH",
#        "filters": {"price": {
#              "max": 150,
#              "min": 100
#           }}
#     }
#
#
#     response2 = requests.request("POST", url2, json=payload, headers=headers)
#
#     pprint.pprint(response2.text)
#
#
# print('\n\n\n\n\n\n')
#
#
#
# url3 = 'https://hotels4.p.rapidapi.com/properties/v2/detail'
#
# params = {}

url = "https://hotels4.p.rapidapi.com/locations/v3/search"

querystring = {"q": "{}".format('рига'), "locale": "ru_RU", "langid": "1033", "siteid": "300000001"}

headers = {
    "X-RapidAPI-Key": "14cb351c01msh1c48214e3041834p18ae28jsndbaf16e16c16",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
data = json.loads(response.text)

pprint.pprint(response.text)
print(data['sr'][0]['gaiaId'])
print('\n\n\n\n')
url = "https://hotels4.p.rapidapi.com/properties/v2/list"

headers = {
    "X-RapidAPI-Key": "14cb351c01msh1c48214e3041834p18ae28jsndbaf16e16c16",
    "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}
payload = {
    "currency": "USD",
    "eapid": 1,
    "locale": "ru_RU",
    "siteId": 300000001,
    "destination": {"regionId": "{}".format(str(data['sr'][0]['gaiaId']))},
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
data = json.loads(response.text)
with open('data.json', 'w', encoding='utf8') as file:
    json.dump(data, file, indent=8)
pprint.pprint(response.text)



print('\n\n\n\n\n')


url3 = 'https://hotels4.p.rapidapi.com/properties/v2/detail'

hotel_params = {"id": "526046"}
response3 = requests.request("POST", url3, json=hotel_params, headers=headers)



