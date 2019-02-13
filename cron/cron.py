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
sys.stdout.write('\rRequest {}/{} [{}] {}% '.format(0,n_req,' '*100, 0))
for k,request in enumerate(req):
    if request.uniqueDate:
        travels = Travel.get_all_travels(
            request.date, request.origin.code, request.destination.code)
        n_travels = len (travels)
        for j,travel in enumerate(travels):
            travel.save_to_database()
            perc = 100*(k/n_req+(j+1)/(n_travels*n_req))
            sys.stdout.write('\rRequest {0}/{1} [{2}{3}] {4:.2f}% '.format(k+1,n_req,'#'*int(round(perc,0)), ' '*int(round(100-perc,0)), perc))
    else:
        if dt.datetime.now() < request.date  :
            dates = [request.date + dt.timedelta(days=i)
                    for i in range(request.gapTime)]
        else :
            delta = request.date.now() - request.date
            dates = [request.date.now() + dt.timedelta(days=i)
                    for i in range(request.gapTime-delta.days)]
        n_dates = len(dates)
        for i,date in enumerate(dates):
            travels = Travel.get_all_travels(
                date, request.origin.code, request.destination.code)
            n_travels=len(travels)
            for j,travel in enumerate(travels):
                travel.save_to_database()
                perc = 100*(k/n_req+i/(n_dates*n_req)+(j+1)/(n_dates*n_travels*n_req))
                sys.stdout.write('\rRequest {0}/{1} [{2}{3}] {4:.2f}% '.format(k+1,n_req,'#'*int(round(perc,0)), ' '*int(round(100-perc,0)), perc))