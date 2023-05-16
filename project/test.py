import json
import pprint
from aiogram import types

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

#get addres (+ надо достать рейтинг и цену)


def get_overview(hotel_id):
    url3 = 'https://hotels4.p.rapidapi.com/properties/v2/detail'

    hotel_params = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": hotel_id
    }
    response3 = requests.request("POST", url3, json=hotel_params, headers=headers)
    data = json.loads(response3.text)
    with open('data2.json', 'w', encoding='utf8') as file:
        json.dump(data, file, indent=8)


    address = data['data']['propertyInfo']['summary']['location']['address']['addressLine']

    return address

def get_photo(hotel_id):
    url3 = 'https://hotels4.p.rapidapi.com/properties/v2/detail'
    i_num = 3
    hotel_params = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": "526046"
    }
    response3 = requests.request("POST", url3, json=hotel_params, headers=headers)
    data = json.loads(response3.text)
    img = [types.InputMediaPhoto(media=data['data']['propertyInfo']['propertyGallery']['images'][i_num]['image']['url'],
                                 caption=data['data']['propertyInfo']['propertyGallery']['images'][i_num]['image'][
                                     'description'])
           for i_num in range(3)]
    return img


# url = "https://hotels4.p.rapidapi.com/locations/v3/search"

querystring = {"q": "{}".format('рига'), "locale": "ru_RU", "langid": "1033", "siteid": "300000001"}

url = "https://hotels4.p.rapidapi.com/locations/v3/search"

headers = {
	"X-RapidAPI-Key": "f573b57c50msh82289a227babadap1c9622jsn494d656e7e5a",
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com"
}

# headers = {
#     "X-RapidAPI-Key": "f573b57c50msh82289a277babadap1c9622jsn494d656e7e5a",
#     "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
# }
# 14cb351c01msh1c48214e3041834p18ae28jsndbaf16e16c16
response = requests.request("GET", url, headers=headers, params=querystring)
data = json.loads(response.text)

# pprint.pprint(response.text)
# print(data['sr'][0]['gaiaId'])

url = "https://hotels4.p.rapidapi.com/properties/v2/list"

headers = {
    "X-RapidAPI-Key": "f573b57c50msh82289a227babadap1c9622jsn494d656e7e5a",
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
        "max": 200,
        "min": 1
    }}
}

response = requests.request("POST", url, json=payload, headers=headers)
data = json.loads(response.text)
with open('data.json', 'w', encoding='utf8') as file:
    json.dump(data, file, indent=8)
# pprint.pprint(response.text)
print('\n\n\n\n\n')
# список названий отелей
hotel_count = 3
photo = ['да', '3']
photo_count = 3
hotel_list = [
    {data["data"]["propertySearch"]["properties"][i_num]["name"]:{
        'id': data["data"]["propertySearch"]["properties"][i_num]["id"],
        'min_price': data["data"]["propertySearch"]["properties"][i_num]["mapMarker"]["label"]
    }
    for i_num in range(hotel_count)}
]
for hotel, desc in hotel_list[0].items():
    desc['address'] = get_overview(desc['id'])
    desc['photo'] = get_photo(desc['id'])


pprint.pprint(hotel_list)

for hotel, desc in hotel_list[0].items():
    answer = 'название: {name}\n' \
             'цена: {price}\n' \
             'адрес: {address}\n\n\n'.format(name=hotel,
         price=desc['min_price'],
         address=desc['address'],
         # photo=list(desc['photo'][i_num]['media'] for i_num in range(3))
    )
    photo_group = []
    for photo in desc['photo']:
        photo_group.append(photo)


    print(answer)
    print(photo_group)

# answer_text = 'По вашему запросу найден результат:\n'
#
# for hotel, desc in hotel_list[0].items():
#     answer_text += "\tНазвание отеля: {name}\n" \
#                        "\t\tЦена: {price}\n" \
#                    "\t\tАдрес: {address}\n".format(
#         name=hotel,
#         price=desc['min_price'],
#         address=get_overview(hotel_id=desc['id'])
#     )
#
# print(answer_text)











