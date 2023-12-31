from datetime import datetime
from os import getenv

from dotenv import load_dotenv
from peewee import (CharField, DateTimeField, DecimalField, ForeignKeyField,
                    Model)

from connect_db import connect_to_postgre_db

load_dotenv()


db = connect_to_postgre_db(
    db_name=getenv('DB_NAME'),
    db_user=getenv('POSTGRES_USER'),
    db_password=getenv('POSTGRES_PASSWORD'),
    db_host=getenv('DB_HOST'),
    db_port=getenv('DB_PORT')
)


class City(Model):
    name = CharField()
    lat = DecimalField()
    lon = DecimalField()

    class Meta:
        database = db


class WeatherCall(Model):
    time = DateTimeField(default=datetime.now())
    temp = DecimalField()
    temp_min = DecimalField()
    temp_max = DecimalField()
    humidity = CharField()
    city = ForeignKeyField(
        City,
        on_delete='CASCADE',
        related_name='weather_calls',
    )

    class Meta:
        database = db
