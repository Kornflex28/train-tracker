from flask import Flask, render_template
from flask_restful import Resource, Api, reqparse
from mongoengine import *

import json
import datetime as dt

import sys
sys.path.append('..')

from database.Request import Request
from database.Station import Station


import utils.credentials

app = Flask(__name__)
api = Api(app)

# request parser
parser = reqparse.RequestParser()
parser.add_argument(name='origin', type=str, required=True, help="The code of the origin station")
parser.add_argument(name='destination', type=str, required=True, help="The  code of the destination station")
parser.add_argument(name='date', type=str, required=True,
                    help="The date of the first request; format : '%Y-%m-%d %H:%M:%S'")
parser.add_argument(name='gapTime', type=int,
                    help="The number of days you want to execute the request; 0 just for once")


# Requests
# shows a list of request and lets you POST to add new requests
class Requests(Resource):

    @staticmethod
    def get():
        return json.loads(Request.objects.to_json())

    @staticmethod
    def post():
        args = parser.parse_args()
        if args['gapTime'] is None:
            args['gapTime'] = 0

        if args['gapTime'] == 0:
            unique_date = True
        else:
            unique_date = False

        # errors Handled
        origin_station = Station().get_name_by_code(code=args['origin'])
        destination_station = Station().get_name_by_code(code=args['destination'])

        request = Request(origin=origin_station,
                          destination=destination_station,
                          uniqueDate=unique_date, date=dt.datetime.strptime(args['date'], "%Y-%m-%d %H:%M:%S"),
                          gapTime=args['gapTime'])
        request.save()
        return request.to_json(), 201


api.add_resource(Requests, '/requests')


# Request
# shows a single request item and lets you delete a request item
class Request(Resource):

    def get(self, request_id):
        return

    def delete(self, request_id):
        return

    def put(self, request_id):
        return


api.add_resource(Request, '/requests/<request_id>')


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home")



@app.route("/about")
def about():
    return render_template("about.html", title="About")


if __name__ == '__main__':
    app.run(port='8080', debug=True)

