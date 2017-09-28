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
        self.query_statistics('london', 'region')





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
        client.close()
        return {
            'records': resut_arr,
            'region': positions,
            'cityId': cityId
        }

    def queryStreetSets(self, cityId, startIndex, number, condition):
        client = MongoClient(HOST, PORT)
        db = client[DBNAME]
        collection_name = None
        confs = self.base_conf['conf']
        for item in confs:
            if item['id'] == cityId:
                collection_name = item['osm_street_collection']
                way_collection = db[collection_name]
        if collection_name == None:
            return None
        result_arr = []
        smallest_img_number = 40
        total_number = 0
        query_condition = ''
        if condition == 'img_len':
            query_condition = 'attr.'+ 'img_len'
        else:
            query_condition = 'statistics.' + condition
        count = way_collection.find({'attr.img_len': {'$gt': smallest_img_number}}).count()
        for record in way_collection.find({'attr.img_len': {'$gt': smallest_img_number}}).sort(query_condition, -1).skip(startIndex):
            if total_number >= number:
                break
            del record['_id']
            result_arr.append(record)
            total_number += 1

        return {
            "records": result_arr,
            "total": count
        }

    def query_adregion_sets(self, cityId, startIndex, number, condition):
        start_time = time.time()
        client = MongoClient(HOST, PORT)
        db = client[DBNAME]
        collection_name = None
        confs = self.base_conf['conf']
        query_condition = 'statistics.' + condition
        region_collection = None
        for item in confs:
            if item['id'] == cityId:
                collection_name = item['region_collection']
                region_collection = db[collection_name]

                # return None
        result_arr = []

        total_number = 0
        for record in region_collection.find().sort(query_condition, -1).skip(startIndex):
            if total_number >= number:
                break
            img_len = 0
            for images in record['imageList']:
                img_len += len(images['images'])
            record['img_len'] = img_len

            del record['_id']
            del record['image_list']
            del record['streets_ids']
            # record['subRegion'] = []

            record['imageList'] = []

            result_arr.append(record)
            total_number += 1
        end_time = time.time()
        print(end_time - start_time)
        print(number, total_number, region_collection.count())
        return {
            "records": result_arr,
            "total": region_collection.count()
        }

    def _queryNearbyImages(self, cityId, position, distance):
        pass
    def query_statistics(self, cityId, type):
        client = MongoClient(HOST, PORT)
        db = client[DBNAME]
        collection_attr = None
        if type == 'region':
            collection_attr = 'region_collection'
        elif type == 'street':
            collection_attr = 'osm_street_collection'

        confs = self.base_conf['conf']

        collection = None
        for item in confs:
            if item['id'] == cityId:
                collection_name = item[collection_attr]
                collection = db[collection_name]

        if collection == None:
            return None

        result = []

        for record in collection.find():
            id = None
            if 'rid' in record:
                id = record['rid']
            else:
                id = record['id']

            statistics = record['statistics']
            if statistics == None:
                continue
            statistics['id'] = id
            statistics['cityId'] = cityId
            #  hack
            rd = {
                'record':{
                    'lv': record['lv'], 'sv': record['sv'],
                    'statistics': statistics, 'standard': record['standard']},
                'cityObj': {'id':cityId}}
            # statistics['record'] =
            result.append(rd)
        client.close()
        return result

    # def query_all_statistics(self):
    #
    #     client = MongoClient(HOST, PORT)
    #     db = client[DBNAME]
    #     collection_attr = None
    #     collection_attr = 'region_collection'
    #     confs = self.base_conf['conf']
    #     result = []
    #
    #     for item in confs:
    #         collection_name = item[collection_attr]
    #         collection = db[collection_name]
    #         _result = []
    #         _sum_statistics = {}
    #         _number = collection.count()
    #         for record in collection.find():
    #             id = None
    #             if 'rid' in record:
    #                 id = record['rid']
    #             else:
    #                 id = record['id']
    #
    #             statistics = record['statistics']
    #             if statistics == None:
    #                 continue
    #             for attr in statistics:
    #                 if attr not in _sum_statistics:
    #                     _sum_statistics[attr] = 0
    #                 _sum_statistics[attr] += statistics[attr]
    #
    #
    #             statistics['id'] = id
    #             statistics['cityId'] = item['id']
    #             #  hack
    #             rd = {
    #                 'record': {
    #                     'lv': record['lv'], 'sv': record['sv'],
    #                     'statistics': statistics, 'standard': record['standard']},
    #                 'cityObj': {'id': item['id']}}
    #             _result.append(rd)
    #         for attr in _sum_statistics:
    #             _sum_statistics[attr] = _sum_statistics[attr] / _number
    #         # attribute name hack
    #         result.append({
    #             'id': item['id'],
    #             'city': item['id'],
    #             'streets': _result,
    #             'record': {'statistics': _sum_statistics}
    #         })
    #     return result

    def query_all_statistics(self):
        client = MongoClient(HOST, PORT)
        db = client[DBNAME]
        collection_attr = 'all_city_statistics'
        collection = db[collection_attr]
        result = []
        for record in collection.find():
            print(record['id'])
            del record['_id']
            result.append(record)
        return result

# Hack
dataService = DataService('app/conf/')

if __name__ == '__main__':
    dataService = DataService('conf/')
    print(dataService.getConfigJson())