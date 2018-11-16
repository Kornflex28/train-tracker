import json
import re


class Station:
    """
    Static class which allows to search for train station.
    """

    json_station_by_code = json.load(open('station.json'))
    json_station_by_name = {v: k for k, v in json_station_by_code.items()}

    @staticmethod
    def get_name_by_code(code: str) -> str:
        """
        Get the name of the train station with its code
        :param code: Code of the train station (i.e. FRADI)
        :return: The name of the train station
        """
        if code in Station.json_station_by_code:
            return Station.json_station_by_code[code]
        raise ValueError('This code doesn\'t exist')

    @staticmethod
    def get_code_by_name(name: str) -> str:
        """
        Get the name of the train station with its name
        :param name: The train station name (i.e. Dunkerque (Hauts-de-France))
        :return: The code of the train station
        """
        if name in Station.json_station_by_name:
            return Station.json_station_by_name[name]
        raise ValueError('This name doesn\'t exist')

    @staticmethod
    def search_station(search_term: str) -> list:
        """
        Search in the train station names a specific term.
        :param search_term: Term to search in all train station names
        :return: List of corresponding train station. Each element is a diction-
        nary containing the keys: name and code
        """
        selected_stations = []
        if len(search_term) > 1:
            for name in Station.json_station_by_name.keys():
                if re.search(search_term, name, re.IGNORECASE):
                    selected_stations.append(
                        {'name': name,
                         'code': Station.json_station_by_name[name]})
        return selected_stations
