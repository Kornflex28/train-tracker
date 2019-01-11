import datetime as dt
import sys

#sys.path.append("/root/train-tracker/")
sys.path.append("..")

import utils.credentials
from utils.date import DateTime
from travel import Travel
from database.Request import Request as dbRequest



req = dbRequest.objects()
for request in req:
    if request.uniqueDate:
        travels = Travel.get_all_travels(
            request.date, request.origin.code, request.destination.code)
        for travel in travels:
            travel.save_to_database()
    else:
        dates = [dt.datetime.now() + dt.timedelta(days=i)
                 for i in range(request.gapTime)]
        for date in dates:
            travels = Travel.get_all_travels(
                date, request.origin.code, request.destination.code)
            for travel in travels:
                travel.save_to_database()
