# -*- coding: UTF-8 -*-
from app import app, mongo
import json
from flask import request

from app.DataService.DataService import dataService


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
    query_result = dataService.getAllResult(post_data['cityId'])
    return json.dumps(query_result)

@app.route('/regionquery',  methods=['POST'])
def regionQuery():
    post_data = json.loads(request.data.decode())
    print(post_data)
    query_result = dataService.queryRegion(post_data['cityId'], post_data['positions'])
    return json.dumps('query test')


if __name__ == '__main__':
    pass

