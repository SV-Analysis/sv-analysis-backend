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
        # Hack
        attrs = ['green', 'sky', 'road', 'building']
        client = MongoClient(HOST, PORT)
        db = client[DBNAME]
        collection_name = None

        confs = self.base_conf['conf']
        for item in confs:
            if item['id'] == cityId:
                collection_name = item['result_c']
        collection = db[collection_name]
        resut_arr = []
        start_time = time.time()
        for record in collection.find():
            lo = record['location'][0]
            la = record['location'][1]
            max_num = -1
            max_attr = None
            for attr in attrs:
                if max_num < record[attr]:
                    max_num = record[attr]
                    max_attr = attr
            resut_arr.append([la, lo, max_attr])
        print(time.time() - start_time)
        return resut_arr

    def getAllResultImprove(self, cityId):
        start_time = time.time()
        client = MongoClient(HOST, PORT)
        db = client[DBNAME]
        collection_name = None
        confs = self.base_conf['conf']
        for item in confs:
            if item['id'] == cityId:
                collection_name = item['overall_result']
        collection = db[collection_name]

        split_result = []
        for record in collection.find():
            del record['_id']
            split_result += record['seg']

        print(time.time() - start_time)
        return split_result

    def queryRegion(self, cityId, positions):
        # Hack
        if len(positions) <= 2:
            return
        region_boundaries = [[position['lng'], position['lat']] for position in positions]
        client = MongoClient(HOST, PORT)
        db = client[DBNAME]
        collection_name = None
        confs = self.base_conf['conf']
        for item in confs:
            if item['id'] == cityId:
                collection_name = item['result_c']
        collection = db[collection_name]
        resut_arr = []
        start_time = time.time()

        for record in collection.find({
            'location': {
                '$geoWithin': {
                    '$polygon':
                        region_boundaries
                }
            }
        }):
            del record['_id']
            resut_arr.append(record)
        print(time.time() - start_time)
        return {
            'records': resut_arr,
            'region': positions,
            'cityId': cityId
        }

# Hack
dataService = DataService('app/conf/')

if __name__ == '__main__':
    dataService = DataService('conf/')
    print(dataService.getConfigJson())