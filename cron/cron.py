import sys
import utils.credentials

sys.path.append(PATH)

import datetime as dt

from database.Request import Request as dbRequest
from travel import Travel
from utils.date import DateTime
import datetime as dt


import utils.credentials
req = dbRequest.objects()
for request in req:
    if request.uniqueDate:
        travels = Travel.get_all_travels(request.date, request.origin.code, request.destination.code)
        for travel in travels:
            travel.save_to_database()
    else:
        dates = [dt.datetime.now() + dt.timedelta(days=i)
                 for i in range(request.gapTime)]
        for date in dates:
            travels = Travel.get_all_travels(date, request.origin.code, request.destination.code)
            for travel in travels:
                travel.save_to_database()
