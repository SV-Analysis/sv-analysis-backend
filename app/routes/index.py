# -*- coding: UTF-8 -*-
from app import app, mongo
import json
from flask import request
from app.DB.DataService import data_service

@app.route('/')
def index():
    print('here')
    return app.send_static_file('index.html')

@app.route('/test')
def getStationConfig():
    return json.dumps("test")

if __name__ == '__main__':
    pass

