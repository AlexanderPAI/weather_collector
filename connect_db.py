from peewee import PostgresqlDatabase, SqliteDatabase


def connect_to_postgre_db(
        db_name: str,
        db_user: str,
        db_password: str,
        db_host: str,
        db_port: str
):
    return PostgresqlDatabase(
        database=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )


def connect_to_sqlite_db():
    return SqliteDatabase('wcollector.db')
