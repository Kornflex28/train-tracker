from database.Station import *
import json

stations = json.load(open('station.json'))

for code, name in stations.items():
    Station(code=code, name=name).save()
