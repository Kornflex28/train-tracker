from mongoengine import *


class Station(Document):
    code = StringField()
    name = StringField()

    @staticmethod
    def get_name_by_code(code: str) -> str:
        """
        Get the name of the train station with its code
        :param code: Code of the train station (i.e. FRADI)
        :return: The name of the train station
        """
        station = Station.objects(code=code).first()
        if station is None:
            raise ValueError('The code {} doesn\'t exist'.format(code))
        return station.name

    @staticmethod
    def get_code_by_name(name: str) -> str:
        """
        Get the name of the train station with its name
        :param name: The train station name (i.e. Dunkerque (Hauts-de-France))
        :return: The code of the train station
        """
        station = Station.objects(name=name).first()
        if station is None:
            raise ValueError('The name {} doesn\'t exist'.format(name))
        return station.code

    @staticmethod
    def search_station(search_term: str) -> list:
        """
        Search in the train station names a specific term.
        :param search_term: Term to search in all train station names
        :return: List of corresponding train station. Each element is a diction-
        nary containing the keys: name and code
        """
        return Station.objects(name__icontains=search_term)