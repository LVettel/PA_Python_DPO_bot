import datetime

from peewee import *

db = SqliteDatabase('searches.db')

class SearchConfig(Model):
    telegram_id = IntegerField(verbose_name='адрес пользователя')
    command = CharField(max_length=20, null=False, blank=False, verbose_name='изначальная команда поиска')
    city = CharField(max_length=50, null=False, blank=False, verbose_name='искомый город')
    rooms = IntegerField(default=1, verbose_name='количество комнат')
    in_date = DateField(default=datetime.datetime.now(), verbose_name='дата заселения')
    out_date = DateField(default=datetime.datetime.now(), verbose_name='дата уезда')

    class Meta:
        database = db

class Results(Model):
    name = CharField(max_length=120, null=False, blank=False, verbose_name='название отеля')
    min_price = IntegerField(default=1, null=False, verbose_name='минимальная цена')
    address = TextField(null=False, verbose_name='адрес отеля')
    photo = TextField(null=False, verbose_name='фотографии отеля')
    config = ForeignKeyField(SearchConfig, verbose_name='конфигурация поиска')
    class Meta:
        database = db



SearchConfig.create_table()
Results.create_table()



def config_create(data: dict):
    SearchConfig.create(
    telegram_id = data['user_id'],
    command = data['command'],
    city = data['city_name'],
    rooms = data['rooms'],
    in_date = data['in_date'],
    out_date = data['out_date'],
    )
    return SearchConfig.select('id').where(
        SearchConfig.telegram_id == data['user_id'],
        SearchConfig.command == data['command'],
        SearchConfig.city == data['city_name'],
        SearchConfig.rooms == data['rooms'],
        SearchConfig.in_date == data['in_date'],
        SearchConfig.out_date == data['out_date'],
        )



def results_create(data: list, photo_group: list, config_id):
    for hotel, desc in data[0].items():
        Results.create(name=hotel,
                       min_price=desc['min_price'],
                       address=desc['address'],
                       photo=photo_group,
                       config=config_id
                       )



def get_history(user_id):
    return SearchConfig.select().where(SearchConfig.telegram_id == user_id)
