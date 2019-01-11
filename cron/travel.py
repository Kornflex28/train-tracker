from utils.date import DateTime
import requests
from database.Station import Station
from database.TrainRecord import TrainRecord
from database.Proposition import Proposition,Propositions


class Travel:

    url = 'https://www.oui.sncf/proposition/rest/search-travels/outward'

    def __init__(self, departure_date: DateTime, arrival_date: DateTime,origin_code: str, destination_code: str,
                 duration: int, propositions: list):
        self.departure_date = departure_date
        self.arrival_date = arrival_date
        self.origin_code = origin_code
        self.destination_code = destination_code
        self.duration = duration
        self.recorded_date = DateTime.now()
        self.propositions = propositions

    def save_to_database(self):
        list_of_proposition = []
        for proposition in self.propositions:
            p = Proposition(type=proposition['type'],
                            amount=proposition['amount'],
                            remainingSeat=proposition['remaining_seat'])
            p.save()
            list_of_proposition.append(p)
        propositions = Propositions(recordedTime=self.recorded_date, content=list_of_proposition)
        propositions.save()
        
        # tr = TrainRecord(departureTime=self.departure_date,
        #                 arrivalTime=self.arrival_date,
        #                 origin=Station.get_station_by_code(self.origin_code),
        #                 destination=Station.get_station_by_code(self.destination_code),
        #                 duration=self.duration,
        #                 recordedTime=self.recorded_date,)
        # tr.save()
        tr = TrainRecord.objects(departureTime=self.departure_date,
                         arrivalTime=self.arrival_date,
                         origin=Station.get_station_by_code(self.origin_code),
                         destination=Station.get_station_by_code(self.destination_code))
        if not tr :
            tr = TrainRecord(departureTime=self.departure_date,
                         arrivalTime=self.arrival_date,
                         origin=Station.get_station_by_code(self.origin_code),
                         destination=Station.get_station_by_code(self.destination_code),
                         duration=self.duration,
                         propositions=[propositions])
            tr.save()
        else:
            tr.update_one(push__propositions=propositions)
        return tr

    @staticmethod
    def get_all_travels(date: DateTime, origin_code: str, destination_code: str):
        current_date = DateTime(date.year, date.month, date.day, 2, 0)
        dic_of_travels = {}
        while True:
            response = Travel.search(current_date, origin_code, destination_code)
            for resp in response:
                if not resp['id'] in dic_of_travels:
                    dic_of_travels[resp['id']] = resp
            
            if current_date.to_tdate() == response[-1]['departureDate']:
                break
            current_date = DateTime.tdate_to_datetime(response[-1]['departureDate'])
        return [Travel._dic_to_travel(v, origin_code, destination_code) for k, v in dic_of_travels.items()]

    @staticmethod
    def _dic_to_travel(dic, origin_code, destination_code):
        propositions = []
        for proposition in dic['priceProposals']:
            propositions.append({'type': proposition['type'], 'amount': proposition['amount'], 'remaining_seat': proposition['remainingSeat']})
        t = Travel(departure_date=DateTime.tdate_to_datetime(dic['departureDate']),
                   arrival_date=DateTime.tdate_to_datetime(dic['arrivalDate']),
                   origin_code=dic['originStationCode'],
                   destination_code=dic['destinationStationCode'],
                   duration=dic['minuteDuration'],
                   propositions=propositions)
        return t

    @staticmethod
    def search(date: DateTime, origin_code: str, destination_code: str) \
            -> list:
        """
        Search for trains
        :param date: date to search, datetime object
        :param origin_code: code of the origin (i.e. FRXXX)
        :param destination_code: code of the destination (i.e. FRXXX)
        :return: list of available trains
        """
        origin = {"code": origin_code,
                  "name": Station.get_name_by_code(origin_code)}
        destination = {"code": destination_code,
                       "name": Station.get_name_by_code(destination_code)}
        response_json = Travel._query(date, origin, destination).json()
        if "trainProposals" in response_json:
            trains = response_json["trainProposals"]
            return trains
        else:
            raise ValueError('Bad response from request')

    @staticmethod
    def _query(date: DateTime, origin: dict, destination: dict) \
            -> requests.models.Response:
        """
        Request the API to get all travels
        :param date: date to search, datetime object
        :param origin: dictionary with name and code
        :param destination: dictionary with name and code
        :return: Response of the request
        """
        headers = {'Content-Type': 'application/json', }
        data = Travel._create_data(date, origin, destination)
        response = requests.post(Travel.url, headers=headers, data=data)
        return response

    @staticmethod
    def _create_data(date: DateTime, origin: dict, destination: dict) -> str:
        """
        Create the request data
        :param date: date to search, datetime object
        :param origin: dictionary with name and code
        :param destination: dictionary with name and code
        :return: return the data field
        """
        data = '{"origin":"' + origin['name'] + '",' \
               '"originCode":"' + origin['code'] + '",' \
               '"originLocation":{"id":null,"label":null,"longitude":null,' \
               '"latitude":null,"type":"G","country":null,' \
               '"stationCode":"' + origin['code'] + '","stationLabel":null},' \
               '"destination":"' + destination['name'] + '",' \
               '"destinationCode":"' + destination['code'] + '",' \
               '"destinationLocation":' \
               '{"id":null,' \
               '"label":null,' \
               '"longitude":null,' \
               '"latitude":null,' \
               '"type":"G",' \
               '"country":null,' \
               '"stationCode":"' + destination['code'] + '",' \
               '"stationLabel":null},' \
               '"via":null,' \
               '"viaCode":null,' \
               '"viaLocation":null,' \
               '"directTravel":false,' \
               '"asymmetrical":false,' \
               '"professional":false,' \
               '"customerAccount":false,' \
               '"oneWayTravel":true,' \
               '"departureDate":"' + date.to_tdate() + '",' \
               '"returnDate":null,' \
               '"travelClass":"SECOND",' \
               '"country":"FR",' \
               '"language":"fr",' \
               '"busBestPriceOperator":null,' \
               '"passengers":' \
               '[{"travelerId":null,' \
               '"profile":"YOUNG",' \
               '"age":null,' \
               '"birthDate":null,' \
               '"fidelityCardType":"NONE",' \
               '"fidelityCardNumber":null,' \
               '"commercialCardNumber":"",' \
               '"commercialCardType":"YOUNGS",' \
               '"promoCode":null,' \
               '"lastName":null,' \
               '"firstName":null,' \
               '"phoneNumer":null,' \
               '"hanInformation":null}],' \
               '"animals":[],' \
               '"bike":"NONE",' \
               '"withRecliningSeat":false,' \
               '"physicalSpace":null,' \
               '"fares":[],' \
               '"withBestPrices":false,' \
               '"highlightedTravel":null,' \
               '"nextOrPrevious":false,' \
               '"source":"FORM_SUBMIT",' \
               '"targetPrice":null,' \
               '"han":false,' \
               '"outwardScheduleType":"BY_DEPARTURE_DATE",' \
               '"inwardScheduleType":"BY_DEPARTURE_DATE",' \
               '"currency":null,' \
               '"codeFce":null,' \
               '"companions":[],' \
               '"asymetricalItinerary":{}}'
        return data
