import pathlib
import sqlite3
from abc import abstractmethod
from os import getenv

from enum import Enum
from mysql.connector import connect, Error, ProgrammingError


SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()


class DatabaseMixin:
    @abstractmethod
    def connect_to_database(self, database_name, database_exist):
        raise NotImplementedError

    @abstractmethod
    def create_tables(self, queries):
        raise NotImplementedError

    @abstractmethod
    def insert(self, data):
        raise NotImplementedError


class SQLiteDatabase(DatabaseMixin):
    def __init__(self, *args,  **kwargs):
        self.connection = self.connect_to_database(kwargs.get("database_name"), kwargs.get("database_exist"))
        self.event_table_schema = """CREATE TABLE events
             (
                [id] INTEGER PRIMARY KEY,
                [url] text,
                [title] text,
                [date] text,
                [time] text,
                [venue] text,
                [street_address] text,
                [city] text,
                [state] text,
                [zipcode] int,
                [map_url] text,
                [price] text
             )
        """
        self.create_tables(queries=[self.event_table_schema])

    def connect_to_database(self, database_name, database_exist):
        return sqlite3.connect(f"{SCRIPT_DIR}/{database_name}.db")

    def create_tables(self, queries):
        cursor = self.connection.cursor()
        for query in queries:
            cursor.execute(query)

        self.connection.commit()

    def insert(self, data):
        query =  """
        INSERT INTO `events`
            (`url`, `title`, `date`, `time`, `venue`, `street_address`, 
            `city`, `state`, `zipcode`, `map_url`, `price`)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self.connection.cursor()
        cursor.executemany(query, data)
        self.connection.commit()


class MySQLDatabase(DatabaseMixin):
    def __init__(self, *args,  **kwargs):
        self.connection = self.connect_to_database(kwargs.get("database_name"), kwargs.get("database_exist"))
        self.event_table_schema = """
        CREATE TABLE `events` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `url` TEXT,
            `title` TEXT,
            `date` TEXT,
            `time` TEXT,
            `venue` TEXT,
            `street_address` TEXT,
            `city` TEXT,
            `state` TEXT,
            `zipcode` INT(11),
            `map_url` TEXT,
            `price` TEXT,
            PRIMARY KEY (`id`)
        )"""
        self.create_tables(queries=[self.event_table_schema])

    def connect_to_database(self, database_name, database_exist=True):
        """
        Connect to database, creating the database if it does't exist.

        :param database_name: str representing database name
        :param database_exist: bool representing if exists
        :return: connection: connection to mysql db
        """
        try:
            if database_exist:
                return connect(
                    host="localhost",
                    user=getenv("DATABASE_USER"),
                    password=getenv("DATABASE_PASSWORD"),
                    database=database_name,
                )

            connection = connect(
                host="localhost",
                user=getenv("DATABASE_USER"),
                password=getenv("DATABASE_PASSWORD"),
            )
            create_db_query = f"CREATE DATABASE {database_name}"
            cursor = connection.cursor()
            cursor.execute(create_db_query)
            return connection

        except Error as e:
            print(e)

    def create_tables(self, queries):
        """
        :param connection:
        :param queries:
        :return:
        """
        with self.connection.cursor() as cursor:
            for query in queries:
                try:
                    cursor.execute(query)

                except ProgrammingError as e:
                    if e.errno == 1050:
                        print("Table exists, continuing")
                        continue
                    else:
                        print(query)
                        raise ProgrammingError

            self.connection.commit()

    def insert(self, data):
        query = """
        INSERT INTO `events`
            (`url`, `title`, `date`, `time`, `venue`, `street_address`, 
            `city`, `state`, `zipcode`, `map_url`, `price`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        with self.connection.cursor() as cursor:
            cursor.executemany(query, data)
            self.connection.commit()


class DatabaseType(Enum):
    """
    Enum representing a database type.
    """

    SQLITE = ("sqlite", SQLiteDatabase)
    MYSQL = ("mysql", MySQLDatabase)

    @staticmethod
    def list():
        """
        :return: dir of string representations of database type
        """
        return dict(map(lambda output: (output.value[0], output.value[1]), DatabaseType))


class DatabaseFactory:
    supported_types = DatabaseType.list()

    @staticmethod
    def create_database(*args, **kwargs):
        if kwargs.get("database") not in DatabaseFactory.supported_types.keys():
            raise NotImplemented(f'Database type {kwargs.get("database")} is not yet supported.')

        cls_obj = DatabaseFactory.supported_types[kwargs.get("database")]
        obj = cls_obj(*args, **kwargs)
        return obj
