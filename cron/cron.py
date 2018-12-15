import sys
sys.path.append('..')

import datetime as dt

from database.Request import Request as dbRequest
from cron.travel import Travel
from utils.date import DateTime

import utils.credentials

for request in dbRequest.objects():
    if request.uniqueDate:
        travels = Travel.get_all_travels(request.date, request.origin.code, request.destination.code)
        for travel in travels:
            travel.save_to_database()