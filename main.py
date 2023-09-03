from time import sleep
from logging import basicConfig, error, ERROR


from methods import create_table_if_not_exist, check_or_import_cities_from_file_to_db, get_list_cities, get_weather_call
from models import City, WeatherCall

basicConfig(
    level=ERROR,
    format='%(asctime)s %(levelname)s %(message)s'
)


if __name__ == '__main__':
    create_table_if_not_exist([City, WeatherCall])
    check_or_import_cities_from_file_to_db('cities_list.csv')
    while True:
        print(f'Запрос погоды по списку')
        try:
            cities_list = get_list_cities()
            get_weather_call(cities_list)
        except Exception as er:
            error(er)
        finally:
            print(f'Ответ получен')
            sleep(3600)
