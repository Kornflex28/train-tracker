import json
import re

t = json.load(open('station.json'))
station = {}
for x in t:
    if re.match(r"FR(.*)", x["value"]):
        if not x["value"] in station:
            station[x["value"]] = x["label"]

with open('real_station.json', 'w') as f:
    json.dump(station, f, ensure_ascii=False)
