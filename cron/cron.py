import datetime as dt
import sys,time

#sys.path.append("/root/train-tracker/")
sys.path.append("..")

import utils.credentials
from utils.date import DateTime
from travel import Travel
from database.Request import Request as dbRequest



req = dbRequest.objects()
n_req = len(req)
for k,request in enumerate(req):
    print("Request {}/{}".format(k+1,n_req))
    if request.uniqueDate:
        travels = Travel.get_all_travels(
            request.date, request.origin.code, request.destination.code)
        for travel in travels:
            # travel.save_to_database()
            a=1
    else:
        if dt.datetime.now() < request.date  :
            dates = [request.date + dt.timedelta(days=i)
                    for i in range(request.gapTime)]
        else :
            delta = request.date.now() - request.date
            dates = [request.date.now() + dt.timedelta(days=delta.days)
                    for i in range(request.gapTime)]
        n_dates = len(dates)
        sys.stdout.write('\r[{}] {}% '.format(' '*100, 0))
        for i,date in enumerate(dates):
            travels = Travel.get_all_travels(
                date, request.origin.code, request.destination.code)
            for travel in travels:
                # travel.save_to_database()
                a=1
            sys.stdout.write('\r[{}{}] {}% '.format('#'*int(100*(i+1)/n_dates), ' '*int(100*(1-(i+1)/n_dates)), int(100*(i+1)/n_dates)))