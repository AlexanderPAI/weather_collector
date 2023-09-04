from logging import ERROR, basicConfig, error
from time import sleep

from methods import (check_or_import_cities_from_file_to_db,
                     create_table_if_not_exist, get_list_cities,
                     get_weather_call)
from models import City, WeatherCall


basicConfig(
    level=ERROR,
    format='%(asctime)s %(levelname)s %(message)s'
)


if __name__ == '__main__':
    create_table_if_not_exist([City, WeatherCall])
    check_or_import_cities_from_file_to_db('cities_list.csv')
    while True:
        print('Запрос погоды по списку')
        try:
            cities_list = get_list_cities()
            get_weather_call(cities_list)
        except Exception as er:
            error(er)
        finally:
            print('Ответ получен')
            sleep(3600)
