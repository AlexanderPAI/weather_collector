from methods import create_table_if_not_exist, check_or_import_cities_from_file_to_db, get_list_cities, get_weather_call_one, get_weather_call

from models import City, WeatherCall


if __name__ == '__main__':
    create_table_if_not_exist([City, WeatherCall])
    check_or_import_cities_from_file_to_db('cities_list.csv')
    # cities_list = get_list_cities()
    # city = City.select().where(City.name == 'Moscow').get()
    # # get_weather_call(cities_list)
