from mongoengine import *


class TrainRecord(Document):
    origin = ReferenceField('Station', reverse_delete_rule=DO_NOTHING)
    destination = ReferenceField('Station', reverse_delete_rule=DO_NOTHING)
    duration = IntField()
    propositions = ListField(ReferenceField('Proposition',
                                            reverse_delete_rule=DO_NOTHING))
    departureTime = DateTimeField()
    arrivalTime = DateTimeField()
    recordedTime = DateTimeField()
