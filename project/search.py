from aiogram import types
import requests
import json


def city_search(name: str) -> str:
    """
	Функция поиска нужного города.
	Возвращает id города.
	:param name:
	:return:
	"""
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"

    querystring = {"q": "{}".format(name), "locale": "ru_RU", "langid": "1033", "siteid": "300000001"}

    headers = {
        "X-RapidAPI-Key": "f573b57c50msh82289a227babadap1c9622jsn494d656e7e5a",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data = json.loads(response.text)
    # hotel_search(id=data['sr'][0]['gaiaId'])
    if 'gaiaId' in data['sr'][0]:
        return data['sr'][0]['gaiaId']
    else:
        return 'none'


def hotel_search(id: str,
                 rooms: int,
                 in_date: list,
                 out_date: list,
                 sort: str,
                 photo: list,
                 hotel_count: int,
                 best_deal: bool,
                 max_price: int,
                 ) -> list:
    """
	Функция поиска отелей в найденном городе.
	Возвращает список отсортированных по цене отелей.
    :param bestdeal: bool
    :param hotel_count: int
    :param photo: list
	:param id: str
	:param rooms: int
	:param in_date: list(str)
	:param out_date: list(str)
	:param sort: str
	:return: str
	"""
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
            "max": max_price,
            "min": 1
        }}
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    data = json.loads(response.text)
    hotel_list = [
        {data["data"]["propertySearch"]["properties"][i_num]["name"]: {
            'id': data["data"]["propertySearch"]["properties"][i_num]["id"],
            'min_price': data["data"]["propertySearch"]["properties"][i_num]["mapMarker"]["label"],
            'distance':
                data["data"]["propertySearch"]["properties"][i_num]["destinationInfo"]["distanceFromDestination"][
                    "value"]
        }
            for i_num in range(hotel_count)}
    ]
    for hotel, desc in hotel_list[0].items():
        desc['address'] = get_address(desc['id'])
        desc['photo'] = get_photo(hotel_id=desc['id'],
                                  count_photo=int(photo[1]))

    return hotel_list


def get_address(hotel_id: str) -> list:
    """
    Функция для получения адреса отеля.
    :param hotel_id: str
    :return: list
    """
    url3 = 'https://hotels4.p.rapidapi.com/properties/v2/detail'

    hotel_params = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": hotel_id
    }
    response3 = requests.request("POST", url3, json=hotel_params, headers={
        "X-RapidAPI-Key": "f573b57c50msh82289a227babadap1c9622jsn494d656e7e5a",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}
                                 )
    data = json.loads(response3.text)
    with open('data2.json', 'w', encoding='utf8') as file:
        json.dump(data, file, indent=8)

    address = data['data']['propertyInfo']['summary']['location']['address']['addressLine']

    return address


def get_photo(hotel_id: str, count_photo: int) -> list:
    """
    Функция для получения фотографий отеля.
    :param hotel_id: str
    :param count_photo: int
    :return: list
    """
    url3 = 'https://hotels4.p.rapidapi.com/properties/v2/detail'

    hotel_params = {
        "currency": "USD",
        "eapid": 1,
        "locale": "en_US",
        "siteId": 300000001,
        "propertyId": hotel_id
    }
    response3 = requests.request("POST", url3, json=hotel_params, headers={
        "X-RapidAPI-Key": "f573b57c50msh82289a227babadap1c9622jsn494d656e7e5a",
        "X-RapidAPI-Host": "hotels4.p.rapidapi.com"}
                                 )
    data = json.loads(response3.text)
    img = [types.InputMediaPhoto(
        data['data']['propertyInfo']['propertyGallery']['images'][i_num]['image']['url'],
        caption=data['data']['propertyInfo']['propertyGallery']['images'][i_num]['image']['description'])
        for i_num in range(count_photo)]
    return img
