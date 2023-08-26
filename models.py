from datetime import datetime
from peewee import Model, CharField, DecimalField, ForeignKeyField, DateTimeField, SqliteDatabase


db = SqliteDatabase('wcollector.db')


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
