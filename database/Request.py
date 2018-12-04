from mongoengine import *
from database.Station import Station


class Request(Document):
    origin = ReferenceField(Station, reverse_delete_rule=DO_NOTHING)
    destination = ReferenceField(Station, reverse_delete_rule=DO_NOTHING)
    uniqueDate = BooleanField()
    date = DateField()
    gapTime = IntField()


