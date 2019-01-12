from mongoengine import *

connect('train-tracker')


class Station(Document):
    code = StringField()
    name = StringField()


class TrainRequest(Document):
    origin = ReferenceField('Station', reverse_delete_rule=DO_NOTHING)
    destination = ReferenceField('Station', reverse_delete_rule=DO_NOTHING)
    uniqueDate = BooleanField()
    date = DateField()
    gapTime = IntField()


class Proposition(Document):
    amount = FloatField()
    remainingSeat = IntField()


class TrainRecord(Document):
    origin = ReferenceField('Station', reverse_delete_rule=DO_NOTHING)
    destination = ReferenceField('Station', reverse_delete_rule=DO_NOTHING)
    duration = IntField()
    propositions = ListField(ReferenceField('Proposition',
                                            reverse_delete_rule=DO_NOTHING))
    departureTime = DateTimeField()
    arrivalTime = DateTimeField()
    recordedTime = DateTimeField()
