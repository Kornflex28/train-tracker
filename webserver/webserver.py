from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from mongoengine import *

import json
import datetime as dt

import sys
sys.path.append('..')

from database.Request import Request as dbRequest
from database.Station import Station


import utils.credentials

app = Flask(__name__)
api = Api(app)

# requests parser
requests_parser = reqparse.RequestParser()
requests_parser.add_argument(name='origin', type=str, required=True, help="The code of the origin station")
requests_parser.add_argument(name='destination', type=str, required=True, help="The  code of the destination station")
requests_parser.add_argument(name='date', type=str, required=True,
                    help="The date of the first request; format : '%Y-%m-%d %H:%M:%S'")
requests_parser.add_argument(name='gapTime', default=0, type=int,
                    help="The number of days you want to execute the request; 0 just for once")


# Requests
# shows a list of request and lets you POST to add new requests
class Requests(Resource):

    @staticmethod
    def get():
        return json.loads(dbRequest.objects.to_json())

    @staticmethod
    def post():
        requests_args = requests_parser.parse_args()

        if requests_args['gapTime'] == 0:
            unique_date = True
        else:
            unique_date = False

        origin_station = Station().get_station_by_code(requests_args['origin'])
        destination_station = Station().get_station_by_code(requests_args['destination'])

        request = dbRequest(origin=origin_station,
                          destination=destination_station,
                          uniqueDate=unique_date, date=dt.datetime.strptime(requests_args['date'], "%Y-%m-%d %H:%M:%S"),
                          gapTime=requests_args['gapTime'])
        request.save()
        return json.loads(request.to_json()), 201


api.add_resource(Requests, '/requests')


# Request
# shows a single request item and lets you delete a request item
class Request(Resource):

    @staticmethod
    def get(request_id):
        return json.loads(dbRequest.objects(id=request_id).first().to_json())

    @staticmethod
    def delete(request_id):
        dbRequest.objects(id=request_id).delete()
        return "", 204

    @staticmethod
    def put(request_id):
        requests_args = requests_parser.parse_args()

        if requests_args['gapTime'] == 0:
            unique_date = True
        else:
            unique_date = False

        origin_station = Station().get_station_by_code(requests_args['origin'])
        destination_station = Station().get_station_by_code(requests_args['destination'])

        dbRequest.objects(id=request_id).update_one(set__origin=origin_station,
                          set__destination=destination_station,
                          set__uniqueDate=unique_date,
                          set__date=dt.datetime.strptime(requests_args['date'], "%Y-%m-%d %H:%M:%S"),
                          set__gapTime=requests_args['gapTime'])
        return json.loads(dbRequest.objects(id=request_id).first().to_json())


api.add_resource(Request, '/requests/<string:request_id>')


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home")



@app.route("/about")
def about():
    return render_template("about.html", title="About")


if __name__ == '__main__':
    app.run(port='8080', debug=True)

