from database.Station import *
import json
import credentials


stations = json.load(open('station.json'))

for code, name in stations.items():
    Station(code=code, name=name).save()


