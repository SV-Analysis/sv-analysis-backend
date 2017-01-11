import json
import datetime
from pymongo import MongoClient

# Warning: Should included into the config file
HOST = "127.0.0.1"
PORT = 27017

# Warning, all the collection should be read from the configure files
class DataService():
    """
    The function collection to query data from the Database
    """
    def __init__(self):
        # Warning, need to read from config
        self.__client = MongoClient(HOST, PORT)
        # self.__db = self.__client[DB]



data_service = DataService()


if __name__ == '__main__':
    pass