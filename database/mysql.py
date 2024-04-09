import mysql.connector
from config_data import config
from utils.misc.format_date import datetime_to_str


class MysqlDB:
    COMMAND_TABLE_NAME = 'command_history'
    RESULT_TABLE_NAME = 'result_history'

    def __init__(self, database):
        self.database = database
        if not self.create_database():
            raise Exception('database is absent')
        if not self.create_table_command():
            raise Exception('commands table is absent')
        if not self.create_table_result():
            raise Exception('results table is absent')

    def connect(self, database: str = None):
        if database is None:
            return mysql.connector.connect(
                host=config.MYSQL_CREDS['host'],
                user=config.MYSQL_CREDS['user'],
                password=config.MYSQL_CREDS['password']
            )
        self.database = database
        return mysql.connector.connect(
            host=config.MYSQL_CREDS['host'],
            user=config.MYSQL_CREDS['user'],
            password=config.MYSQL_CREDS['password'],
            database=database
        )

    def create_database(self):
        mydb = self.connect()
        mycursor = mydb.cursor()

        mycursor.execute(f'CREATE DATABASE IF NOT EXISTS {self.database}')
        mycursor.execute(f'SHOW DATABASES')
        exists = False
        for x in mycursor:
            exists = exists or self.database in x

        return exists

    def _connect(self):
        return self.connect(self.database)

    def query(self, q_str: str):
        mydb = self._connect()

        mycursor = mydb.cursor()

        return mycursor.execute(q_str)

    def select(self, q_str: str, one: bool = False):
        mydb = self._connect()

        mycursor = mydb.cursor()

        mycursor.execute(q_str)

        if one:
            return mycursor.fetchone()
        else:
            return mycursor.fetchall()

    def create_table_command(self):
        mydb = self._connect()

        mycursor = mydb.cursor()

        mycursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.COMMAND_TABLE_NAME} "
            "(id INT AUTO_INCREMENT PRIMARY KEY, UserId int, "
            "command varchar(30), date TIMESTAMP NOT NULL "
            "DEFAULT CURRENT_TIMESTAMP, city varchar(30))")

        mycursor.execute(f'SHOW TABLES')
        exists = False
        for x in mycursor:
            exists = exists or self.COMMAND_TABLE_NAME in x

        return exists

    def create_table_result(self):
        mydb = self._connect()

        mycursor = mydb.cursor()

        mycursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.RESULT_TABLE_NAME} "
            "(id INT AUTO_INCREMENT PRIMARY KEY, ComandedId int, hotel varchar(512), "
            f"FOREIGN KEY (ComandedId) REFERENCES {self.COMMAND_TABLE_NAME}(id))")

        mycursor.execute(f'SHOW TABLES')
        exists = False
        for x in mycursor:
            exists = exists or self.RESULT_TABLE_NAME in x

        return exists

    def insert_command(self, user_id, command, city=None):
        mydb = self._connect()

        mycursor = mydb.cursor()
        sql = f"INSERT INTO {self.COMMAND_TABLE_NAME}(UserId, command, city) "
        sql += f"VALUES(%s, %s, %s)"
        val = (user_id, command, city)
        mycursor.execute(sql, val)
        mydb.commit()
        return mycursor.lastrowid

    def update_command(self, history_id, city):
        mydb = self._connect()

        mycursor = mydb.cursor()
        sql = f"UPDATE {self.COMMAND_TABLE_NAME}  "
        sql += f"SET city = %s "
        sql += f"WHERE id = %s "
        val = (city, history_id)
        mycursor.execute(sql, val)
        mydb.commit()

    def insert_result(self, command_id, hotel):
        mydb = self._connect()

        mycursor = mydb.cursor()
        sql = f"INSERT INTO {self.RESULT_TABLE_NAME}(ComandedId, hotel) "
        sql += f"VALUES(%s, %s)"
        val = (command_id, hotel)
        mycursor.execute(sql, val)
        mydb.commit()

    def read_command_for(self, user_id):
        return self.select(
            f"SELECT * "
            f"FROM {self.COMMAND_TABLE_NAME} WHERE UserId = {user_id}"
        )

    def read_results_for(self, command_id):
        return self.select(
            f"SELECT hotel "
            f"FROM {self.RESULT_TABLE_NAME} WHERE ComandedId = {command_id}"
        )

    def display(self, user_id):
        data = self.read_command_for(user_id)
        res = ""
        for record in data:
            res += f"Имя команды: {record[2]}\n"
            res += f"Время вызова команды: {datetime_to_str(record[3])}\n"
            if record[2] != "start":
                res += f'Город: {record[4]}\n'
                res += f"Результаты поиска отелей:\n"
                hotels = self.read_results_for(record[1])

                for k, hotel in enumerate(hotels):
                    res += f'Найденный отель №{str(k+1)} с названием: ' + hotel + '\n'

        return res
