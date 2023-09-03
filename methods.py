from os import getenv
from requests import get
from json import loads
from csv import DictReader
from dotenv import load_dotenv

from models import City, WeatherCall


load_dotenv()


def create_table_if_not_exist(models: list):
    """
    Создание таблиц моделей в случае их остутствия.
    Принимает в качестве параметра models - список моделей.
    """
    for model in models:
        model.create_table()


def check_or_import_cities_from_file_to_db(file, model=City):
    """
    При первом запуске - создает записи городов из *.csv.
    При последующих запусках - проверяет соответствение записей городов
    в БД списку cities_list.csv.
    Вслучае изменении списка в csv, при перезапуске актуализирует список город.
    """
    cities_in_db = [*model.select().execute()]
    cities_list_from_file = []
    cities_to_create = []
    cities_to_delete = []

    for row in DictReader(open(file)):
        api_url = f'http://api.openweathermap.org/geo/1.0/direct?q={row["name"]}&&appid={getenv("API_KEY")}'
        response = get(api_url)
        response = loads(response.text)[0]
        cities_list_from_file.append(
            model(
                name=row['name'],
                lat=response['lat'],
                lon=response['lon'],
            )
        )

    for city in cities_list_from_file:
        city_exist = False
        for city_in_db in cities_in_db:
            if city.name == city_in_db.name:
                city_exist = True
                break
        if city_exist == False:
            cities_to_create.append(city)

    for city_in_db in cities_in_db:
        delete = True
        for city in cities_list_from_file:
            if city_in_db.name == city.name:
                delete = False
                break
        if delete == True:
            cities_to_delete.append(city_in_db.name)

    model.bulk_create(cities_to_create)
    model.delete().where(model.name.in_(cities_to_delete)).execute()


def get_list_cities(model=City):
    """Получить список городов из БД."""
    return [*model.select().execute()]


def get_weather_call(cities_list: list, model=WeatherCall):
    """
    Получает данные о погоде по списку городов, переданному
    в качестве параметра.
    """
    weather_call_result = []
    for city in cities_list:
        url = f'https://api.openweathermap.org/data/2.5/weather?lat={city.lat}&lon={city.lon}&appid={getenv("API_KEY")}'
        response = get(url)
        response = loads(response.text)
        weather_call_result.append(
            model(
                temp=response['main']['temp'],
                temp_min=response['main']['temp_min'],
                temp_max=response['main']['temp_max'],
                humidity=response['main']['humidity'],
                city=city,
            )
        )
    model.bulk_create(weather_call_result)
