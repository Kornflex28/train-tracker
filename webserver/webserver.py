from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask_cors import  CORS
import json
import datetime as dt
from mongoengine import *

import sys
sys.path.append('..')


from database.Request import Request as dbRequest
from database.Station import Station as dbStation
from database.Proposition import Proposition as dbProposition
from database.TrainRecord import TrainRecord as dbTrainRecord

import utils.credentials

app = Flask(__name__)
api = Api(app)
CORS(app)

# Requests
# shows a list of requests and lets you POST to add new requests in the database
class Requests(Resource):

    @staticmethod
    def get():
        """
        Get the list of all the requests registered in the database.
        :return: A list of JSON each containing a request.
        """
        requests = json.loads(dbRequest.objects.to_json())
        #print(json)
        for request in requests :
            #request['date'] = str(dt.datetime.fromtimestamp((request['date']['$date'])))
            request['destination'] = dbStation.objects(id=request['destination']['$oid']).first().name
            request['origin'] = dbStation.objects(id=request['origin']['$oid']).first().name
        return requests, 200

    @staticmethod
    def post():
        """
        Add a NEW request that will be registered in the database.
        :param: Arguments of the POST request.
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

        # gets the corresponding Station object
        origin_station = dbStation().get_station_by_code(requests_args['origin'])
        destination_station = dbStation().get_station_by_code(requests_args['destination'])

        if requests_args['gapTime'] == 0:
            unique_date = True
        else:
            unique_date = False

        # checks if the request already exists in the database
        request_exist = dbRequest.objects(origin=origin_station, destination=destination_station,
                                          uniqueDate=unique_date,
                                          date=dt.datetime.strptime(requests_args['date'], "%Y-%m-%d %H:%M:%S"),
                                          gapTime=requests_args['gapTime']).first() is not None

        if request_exist:
            request_id = dbRequest.objects(origin=origin_station,
                                           destination=destination_station,
                                           uniqueDate=unique_date,
                                           date=dt.datetime.strptime(requests_args['date'], "%Y-%m-%d %H:%M:%S"),
                                           gapTime=requests_args['gapTime']).first().id
            return "The request already exists at id {}".format(request_id), 208
        else:
            request = dbRequest(origin=origin_station,
                                destination=destination_station,
                                uniqueDate=unique_date,
                                date=dt.datetime.strptime(requests_args['date'], "%Y-%m-%d %H:%M:%S"),
                                gapTime=requests_args['gapTime'])
            request.save()

            request = json.loads(request.to_json())
            request['date'] = requests_args['date']
            request['destination'] = destination_station.name
            request['origin'] = origin_station.name
            return request, 201


api.add_resource(Requests, '/requests')


# Request
# shows a single request item and lets you PUT or DELETE a request item in the database
class Request(Resource):

    @staticmethod
    def get(request_id):
        """
        Get a single request registered in the database.
        :param: request_id: Id of the request to get
        :return: A JSON file of the request.
        """
        if dbRequest.objects(id=request_id).first() is not None:
            return json.loads(dbRequest.objects(id=request_id).first().to_json()), 200
        else:
            return "Request not found at this id {}".format(request_id), 404

    @staticmethod
    def delete(request_id):
        """
        Delete from the database a single request registered in the database.
        :param: request_id: Id of the request to delete
        :return: 204.
        """
        dbRequest.objects(id=request_id).delete()
        return "", 204

    @staticmethod
    def put(request_id):
        """
        Update a request that is registered in the database.
        :param: Arguments of the PUT request.
        origin: Code of the origin station (i.e. FRADI) - Default is the request's one
        destination: Code of the destination station (i.e. FRAFJ) - Default is the request's one
        date: Date of the first request with the format %Y-%m-%d %H:%M:%S - Default is the request's one
        gapTime: Number of days you want to execute the request - Default is the request's one
        :return: A JSON file of the request newly updated.
        """

        # request parser
        request_parser = reqparse.RequestParser()
        request_parser.add_argument(name='origin', type=str, help="The code of the origin station")
        request_parser.add_argument(name='destination', type=str, help="The  code of the destination station")
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

        origin_station = dbStation().get_station_by_code(request_args['origin'])
        destination_station = dbStation().get_station_by_code(request_args['destination'])

        dbRequest.objects(id=request_id).update_one(set__origin=origin_station,
                                                    set__destination=destination_station, set__uniqueDate=unique_date,
                                                    set__date=dt.datetime.strptime(request_args['date'],
                                                                                   "%Y-%m-%d %H:%M:%S"),
                                                    set__gapTime=request_args['gapTime'])
        return json.loads(dbRequest.objects(id=request_id).first().to_json()), 200


api.add_resource(Request, '/requests/<string:request_id>')


# Stations
# shows a list of stations and lets you POST to add new stations in the database
class Stations(Resource):
    @staticmethod
    def get():
        """
        Get the list of all the stations registered in the database.
        :return: A list of JSON each containing a station.
        """
        return json.loads(dbStation.objects.to_json()), 200

    @staticmethod
    def post():
        """
        Add a NEW station that will be registered in the database.
        :param: Arguments of the POST request.
                code: Code of the station (i.e. FRAFJ) - Required
                name: Name of the station - Required
        :return: A JSON file of the station newly registered.
        """

        # stations parser
        stations_parser = reqparse.RequestParser()
        stations_parser.add_argument(name='code', type=str, required=True, help="The  code of the station (i.e. FRAFJ)")
        stations_parser.add_argument(name='name', type=str, required=True, help="The name of the station")
        stations_args = stations_parser.parse_args()

        # checks if the station already exists in the database
        station_exist = dbStation.objects(code=stations_args['code'], name=stations_args['name']).first() is not None

        if station_exist:
            station_id = dbStation.objects(code=stations_args['code'], name=stations_args['name']).first().id
            return "The station already exists at id {}".format(station_id), 208
        else:
            station = dbStation(code=stations_args['code'], name=stations_args['name'])
            station.save()
            return json.loads(station.to_json()), 201


api.add_resource(Stations, '/stations')


# Station
# shows a single station item and lets you PUT or DELETE a station item in the database
class Station(Resource):

    @staticmethod
    def get(station_id):
        """
        Get a single station registered in the database.
        :param: station_id: Id of the station to get
        :return: A JSON file of the station.
        """
        if dbStation.objects(id=station_id).first() is not None:
            return json.loads(dbStation.objects(id=station_id).first().to_json()), 200
        else:
            return "Station not found at this id {}".format(station_id), 404

    @staticmethod
    def delete(station_id):
        """
        Delete from the database a single station registered in the database.
        :param: request_id: Id of the station to delete
        :return: 204.
        """
        dbStation.objects(id=station_id).delete()
        return "", 204

    @staticmethod
    def put(station_id):
        """
        Update a station that is registered in the database.
        :param: code: Code of the origin station (i.e. FRADI) - Default is the station's one
                name: Code of the destination station (i.e. FRAFJ) - Default is the station's one
        :return: A JSON file of the station newly updated.
        """

        # station parser
        station_parser = reqparse.RequestParser()
        station_parser.add_argument(name='code', type=str, help="The  code of the station (i.e. FRAFJ)")
        station_parser.add_argument(name='name', type=str, help="The name of the station")
        station_args = station_parser.parse_args()

        station = dbStation.objects(id=station_id).first()

        # get default values
        if station_args['code'] is None:
            station_args['code'] = station.code
        if station_args['name'] is None:
            station_args['name'] = station.name

        dbStation.objects(id=station_id).update_one(set__code=station_args['code'], set__name=station_args['name'])
        return json.loads(dbStation.objects(id=station_id).first().to_json()), 200


api.add_resource(Station, '/stations/<string:station_id>')


# Propositions
# shows a list of propositions and lets you POST to add new propositions in the database
class Propositions(Resource):
    @staticmethod
    def get():
        """
        Get the list of all the propositions registered in the database.
        :return: A list of JSON each containing a proposition.
        """
        return json.loads(dbProposition.objects.to_json()), 200

    @staticmethod
    def post():
        """
        Add a NEW proposition that will be registered in the database.
        :param: Arguments of the POST request.
                amount: Price of the proposition - Required
                remainingSeat: Number of remaining seats for the proposition - Required
        :return: A JSON file of the proposition newly registered.
        """

        # propositions parser
        propositions_parser = reqparse.RequestParser()
        propositions_parser.add_argument(name='amount', type=int, required=True, help="The  price of the proposition")
        propositions_parser.add_argument(name='remainingSeat', type=float, required=True,
                                         help="The  number of remaining seats for the proposition")
        propositions_args = propositions_parser.parse_args()

        # checks if the proposition already exists in the database
        proposition_exist = dbProposition.objects(amount=propositions_args['amount'],
                                                  remainingSeat=propositions_args['remainingSeat']).first() is not None
        print(proposition_exist, dbProposition.objects(amount=propositions_args['amount'],
                                                       remainingSeat=propositions_args['remainingSeat']))
        if proposition_exist:
            proposition_id = dbProposition.objects(amount=propositions_args['amount'],
                                                   remainingSeat=propositions_args['remainingSeat']).first().id
            return "The proposition already exists at id {}".format(proposition_id), 208
        else:
            proposition = dbProposition(amount=propositions_args['amount'],
                                        remainingSeat=propositions_args['remainingSeat'])
            proposition.save()
            return json.loads(proposition.to_json()), 201


api.add_resource(Propositions, '/propositions')


# Proposition
# shows a single proposition item and lets you PUT or DELETE a proposition item in the database
class Proposition(Resource):

    @staticmethod
    def get(proposition_id):
        """
        Get a single proposition registered in the database.
        :param: proposition_id: Id of the proposition to get
        :return: A JSON file of the proposition.
        """
        if dbProposition.objects(id=proposition_id).first() is not None:
            return json.loads(dbProposition.objects(id=proposition_id).first().to_json()), 200
        else:
            return "Proposition not found at this id {}".format(proposition_id), 404

    @staticmethod
    def delete(proposition_id):
        """
        Delete from the database a single proposition registered in the database.
        :param: proposition_id: Id of the proposition to delete
        :return: 204.
        """
        dbProposition.objects(id=proposition_id).delete()
        return "", 204

    @staticmethod
    def put(proposition_id):
        """
        Update a proposition that is registered in the database.
        :param: amount: Price of the proposition - Default is the proposition's one
                remainingSeat: Number of remaining seats for the proposition - Default is the proposition's one
        :return: A JSON file of the proposition newly updated.
        """

        # proposition parser
        proposition_parser = reqparse.RequestParser()
        proposition_parser.add_argument(name='amount', type=int, help="The  price of the proposition")
        proposition_parser.add_argument(name='remainingSeat', type=float,
                                        help="The  number of remaining seats for the proposition")
        proposition_args = proposition_parser.parse_args()

        proposition = dbProposition.objects(id=proposition_id).first()

        # get default values
        if proposition_args['amount'] is None:
            proposition_args['amount'] = proposition.amount
        if proposition_args['remainingSeat'] is None:
            proposition_args['remainingSeat'] = proposition.remainingSeat

        dbProposition.objects(id=proposition_id).update_one(set__amount=proposition_args['amount'],
                                                            set__remainingSeat=proposition_args['remainingSeat'])
        return json.loads(dbProposition.objects(id=proposition_id).first().to_json()), 200


api.add_resource(Proposition, '/propositions/<string:proposition_id>')


# TrainRecords
# shows a list of train records in the database
class TrainRecords(Resource):
    @staticmethod
    def get():
        """
        Get the list of all the train records registered in the database.
        :return: A list of JSON each containing a train record.
        """
        return json.loads(dbTrainRecord.objects.to_json()), 200

api.add_resource(TrainRecords, '/trainrecords')


# TrainRecord
# shows a single train record item and lets you  DELETE a train record item in the database
class TrainRecord(Resource):

    @staticmethod
    def get(trainrecord_id):
        """
        Get a single train record registered in the database.
        :param: trainrecord_id: Id of the train record to get
        :return: A JSON file of the train record.
        """
        if dbTrainRecord.objects(id=trainrecord_id).first() is not None:
            return json.loads(dbTrainRecord.objects(id=trainrecord_id).first().to_json()), 200
        else:
            return "Train record not found at this id {}".format(trainrecord_id), 404

    @staticmethod
    def delete(trainrecord_id):
        """
        Delete from the database a single train record registered in the database.
        :param: trainrecord_id: Id of the train record to delete
        :return: 204.
        """
        dbTrainRecord.objects(id=trainrecord_id).delete()
        return "", 204


api.add_resource(TrainRecord, '/trainrecords/<string:trainrecord_id>')


if __name__ == '__main__':
    app.run(port='8080', debug=True)

