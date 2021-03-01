import pymysql
from typing import List, Dict, Set

#SQL Reader class which is a modified version of the file provided by Alex Geary
class sqlReader:
    connection = pymysql.connections.Connection
    enable_writes = True
    last_query = "NONE"

    # Constructor
    def __init__(self, user_name: str, user_password: str, db_name: str, enable_writes: bool = True):
        self.enable_writes = enable_writes
        self.connection = pymysql.connect(host='localhost', user=user_name, password=user_password, db=db_name, cursorclass=pymysql.cursors.DictCursor)
        self.connection.autocommit(True)

    def read_data(self, sql_str: str) -> Dict:
        self.last_query = sql_str
        with self.connection.cursor() as cursor:
            cursor.execute(sql_str)
            result = cursor.fetchall()
            return result
            
    def write_data(self, sql_str: str):
        self.last_query = sql_str
        if not self.enable_writes:
            return

        with self.connection.cursor() as cursor:
            cursor.execute(sql_str)

    # sql_str:
    # int: return type
    def write_data_get_row_id(self, sql_str: str) -> int:
        self.last_query = sql_str
        if not self.enable_writes:
            return -1

        with self.connection.cursor() as cursor:
            cursor.execute(sql_str)
            return cursor.lastrowid

    # to_escape:
    def escape_text(self, to_escape):
        if type(to_escape) is str:
            return self.connection.escape(to_escape)

        return to_escape

    # Return the last_query of this class instance
    # str: return type
    def get_last_query(self) -> str:
        return self.last_query

    # Close the connection to the database
    def close(self):
        self.connection.close()

    #Extracts the relevant information from the data returned by the SQL query
    def sentenceExtraction(self, data):
        sentences = []
        users = []
        sql = "(SELECT id, name FROM t_user)"
        usernames = self.read_data(sql)
        names = {}
        for user in usernames:
            id = user["id"]
            name = user["name"]
            names[id] = name
        for sentence in data:
            user = sentence["user"]
            sentence = sentence["text"].replace("  ", " ")
            sentences.append(sentence)
            user = names[user]
            users.append(user)
        return sentences, users