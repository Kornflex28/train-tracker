from flask import Flask, request
from flask_restful import Resource, Api
from mongoengine import *
import json

import sys

sys.path.append('..')

from database.Request import Request

app = Flask(__name__)
api = Api(app)
connect('train-tracker')


class Requests(Resource):

    @staticmethod
    def get():
        return json.loads(Request.objects.to_json())


api.add_resource(Requests, '/requests')

if __name__ == '__main__':
    app.run(port='8080')
