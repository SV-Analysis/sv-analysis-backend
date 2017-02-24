# -*- coding: UTF-8 -*-
from app import app
import json
from flask import request
from flask import send_file
from app.DataService.DataService import dataService
from flask import send_file

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/test')
def getStationConfig():
    return json.dumps("test")

@app.route('/readconf')
def getConfInfo():
    config_obj = dataService.getConfigJson()
    return json.dumps(config_obj)

@app.route('/getallrecords',  methods=['POST'])
def getAllRecords():
    post_data = json.loads(request.data.decode())
    query_result = dataService.getAllResultImprove(post_data['cityId'])
    return json.dumps(query_result)

@app.route('/regionquery',  methods=['POST'])
def regionQuery():
    post_data = json.loads(request.data.decode())

    query_result = dataService.queryRegion(post_data['cityId'], post_data['positions'])
    return json.dumps(query_result)

@app.route('/streetsetquery', methods=['POST'])
def steetQuery():
    post_data = json.loads(request.data.decode())
    cityId = post_data['cityId']
    startIndex = post_data['startIndex']
    number = post_data['number']
    query_data = dataService.queryStreetSets(cityId, startIndex, number)
    return json.dumps(query_data);

@app.route('/adregionsetquery', methods=['POST'])
def administrative_region_Query():
    post_data = json.loads(request.data.decode())
    cityId = post_data['cityId']
    startIndex = post_data['startIndex']
    number = post_data['number']
    query_data = dataService.query_adregion_sets(cityId, startIndex, number)
    return json.dumps(query_data)

@app.route('/getImage', methods=['GET', 'POST'])
def getImages():
    image_path = createImageLink(request.args.get('city'),
                                 request.args.get('cid'),
                                 request.args.get('iid'))
    return send_file(image_path, mimetype='image/gif')

def createImageLink(city, cid, iid):
    folder = '../../res/';
    all_path = folder + city + '/images/' + cid + '/' + iid
    return all_path
if __name__ == '__main__':
    pass

