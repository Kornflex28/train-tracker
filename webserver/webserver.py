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


# Requests
# shows a list of requests and lets you POST to add new requests
class Requests(Resource):

    @staticmethod
    def get():
        """
        Get the list of all the requests registered in the database.
        :return: A JSON list of all the requests.
        """
        return json.loads(dbRequest.objects.to_json())

    @staticmethod
    def post():
        """
        Add a NEW request that will be registered in the database.
        :param: You need several arguments to the POST request.
                origin: Code of the origin station (i.e. FRADI) - Required
                destination: Code of the destination station (i.e. FRAFJ) - Required
                date: Date of the first request with the format %Y-%m-%d %H:%M:%S - Required
                gapTime: Number of days you want to execute the request - Default is 0
        :return: A JSON file of the request newly registered.
        """

        # requests parser
        requests_parser = reqparse.RequestParser()
        requests_parser.add_argument(name='origin', type=str, required=True, help="The code of the origin station")
        requests_parser.add_argument(name='destination', type=str, required=True,
                                     help="The  code of the destination station")
        requests_parser.add_argument(name='date', type=str, required=True,
                                     help="The date of the first request; format : '%Y-%m-%d %H:%M:%S'")
        requests_parser.add_argument(name='gapTime', default=0, type=int,
                                     help="The number of days you want to execute the request; 0 just for once")
        requests_args = requests_parser.parse_args()

        # Get the corresponding Station object
        origin_station = Station().get_station_by_code(requests_args['origin'])
        destination_station = Station().get_station_by_code(requests_args['destination'])

        if requests_args['gapTime'] == 0:
            unique_date = True
        else:
            unique_date = False

        # Check if the request already exists in the database
        request_exist = dbRequest.objects(origin=origin_station,
                          destination=destination_station,
                          uniqueDate=unique_date, date=dt.datetime.strptime(requests_args['date'], "%Y-%m-%d %H:%M:%S"),
                          gapTime=requests_args['gapTime']) is not None

        if request_exist:
            request_id = dbRequest.objects(origin=origin_station,
                                           destination=destination_station,
                                           uniqueDate=unique_date,
                                           date=dt.datetime.strptime(requests_args['date'], "%Y-%m-%d %H:%M:%S"),
                                           gapTime=requests_args['gapTime']).first().id
            raise ValueError("The request already exists at id {}".format(request_id))
        else:
            request = dbRequest(origin=origin_station,
                                destination=destination_station,
                                uniqueDate=unique_date,
                                date=dt.datetime.strptime(requests_args['date'], "%Y-%m-%d %H:%M:%S"),
                                gapTime=requests_args['gapTime'])
            request.save()
            return json.loads(request.to_json()), 201


api.add_resource(Requests, '/requests')


# Request
# shows a single request item and lets you PUT or DELETE a request item
class Request(Resource):

    @staticmethod
    def get(request_id):
        """
        Get a single request registered in the database.
        :param: request_id: Id of the request to update
        :return: A JSON list of the request.
        """
        return json.loads(dbRequest.objects(id=request_id).first().to_json())

    @staticmethod
    def delete(request_id):
        """
        Delete from the database a single request registered in the database.
        :param: request_id: Id of the request to delete
        :return: A JSON list of the request.
        """
        dbRequest.objects(id=request_id).delete()
        return "", 204

    @staticmethod
    def put(request_id):
        """
        Update a request that is registered in the database.
        :param: You need several arguments to the PUT request.
        origin: Code of the origin station (i.e. FRADI) - Default is the request's one
        destination: Code of the destination station (i.e. FRAFJ) - Default is the request's one
        date: Date of the first request with the format %Y-%m-%d %H:%M:%S - Default is the request's one
        gapTime: Number of days you want to execute the request - Default is the request's one
        :return: A JSON file of the request newly updated.
        """

        # request parser
        request_parser = reqparse.RequestParser()
        request_parser.add_argument(name='origin', type=str, help="The code of the origin station")
        request_parser.add_argument(name='destination', type=str,
                                     help="The  code of the destination station")
        request_parser.add_argument(name='date', type=str,
                                     help="The date of the first request; format : '%Y-%m-%d %H:%M:%S'")
        request_parser.add_argument(name='gapTime', type=int,
                                     help="The number of days you want to execute the request; 0 just for once")
        request_args = request_parser.parse_args()

        request = dbRequest.objects(id=request_id).first()

        # get default values
        if request_args['origin'] is None:
            request_args['origin'] = request.origin.code
        if request_args['destination'] is None:
            request_args['destination'] = request.destination.code
        if request_args['date'] is None:
            request_args['date'] = dt.datetime.strftime(request.date, "%Y-%m-%d %H:%M:%S")
        if request_args['gapTime'] is None:
            request_args['gapTime'] = request.gapTime

        if request_args['gapTime'] == 0:
            unique_date = True
        else:
            unique_date = False

        origin_station = Station().get_station_by_code(request_args['origin'])
        destination_station = Station().get_station_by_code(request_args['destination'])

        dbRequest.objects(id=request_id).update_one(set__origin=origin_station,
                          set__destination=destination_station,
                          set__uniqueDate=unique_date,
                          set__date=dt.datetime.strptime(request_args['date'], "%Y-%m-%d %H:%M:%S"),
                          set__gapTime=request_args['gapTime'])
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

