from date import Date
import datetime as dt
import requests
from station import Station


class Travel:

    url = 'https://www.oui.sncf/proposition/rest/search-travels/outward'

    @staticmethod
    def search(date: dt.datetime, origin_code: str, destination_code: str) \
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
    def _query(date: dt.datetime, origin: dict, destination: dict) \
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
    def _create_data(date: dt.datetime, origin: dict, destination: dict) -> str:
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
               '"departureDate":"' + Date.datetime_to_tdate(date) + '",' \
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
