from date import Date
import datetime as dt


class Travel:

    @staticmethod
    def _query(date, origin, destination):
        pass

    @staticmethod
    def _create_data(date: dt.datetime, origin: dict, destination: dict) -> str:
        """

        :param date: date to search
        :param origin: dictionary with name and code
        :param destination: dictionary with name and code
        :return:
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
               '"departureDate":"' + Date.date_to_tdate(date) + '",' \
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
