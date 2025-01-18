import pyodbc
from typing import Optional
class DataBase_Connection:
    def __init__(self, server_name: str, driver: str, database_name: str) -> None:
        self._server_name = server_name
        self._driver = driver
        self._database_name = database_name

    @property
    def server_name(self) -> str:
        return self._server_name

    @property
    def driver(self) -> str:
        return self._driver

    @property
    def database_name(self) -> str:
        return self._database_name

    def open_connection(self) -> Optional[pyodbc.Connection]:
        try:
            conn=f"""DRIVER={self.driver}; SERVER={self.server_name};DATABASE={self.database_name};Trusted_Connection=yes;"""
            return conn
        except pyodbc.Error as e:
            print(f"Error connecting to the database: {e}")
            return None
