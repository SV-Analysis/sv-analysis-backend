import json
import time
from pymongo import MongoClient

# Warning: Should included into the config file
HOST = "127.0.0.1"
PORT = 27017
DBNAME = 'sv_analysis'
CONF_PATH = '../../conf'
from  app.conf.Configuration import Configuration
# Warning, all the collection should be read from the configure files
class DataService():
    """
    The function collection to query data from the Database
    """
    def __init__(self, conf_path):
        # Warning, need to read from config
        self.__client = MongoClient(HOST, PORT)
        # self.__db = self.__client[DB]
        self.conf = Configuration()

        # Conf file will be written into database
        self.base_conf = self.conf.read_configuration(conf_path)


    def getConfigJson(self):
        return self.base_conf

    def getAllResult(self, cityId):
        client = MongoClient(HOST, PORT)
        db = client[DBNAME]
        collection_name = None
        for item in self.base_conf:
            if item['id'] == cityId:
                collection_name = item['result_c']
        collection = db[collection_name]
        resut_arr = []
        start_time = time.time()
        for record in collection.find():
            lo = record['location'][1]
            la = record['location'][0]
            resut_arr.append([lo, la])

        print(time.time() - start_time)
        return resut_arr

# Hack
dataService = DataService('app/conf/')

if __name__ == '__main__':
    dataService = DataService('conf/')
    print(dataService.getConfigJson())