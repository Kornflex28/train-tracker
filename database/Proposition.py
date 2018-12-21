from mongoengine import *


class Proposition(Document):
    type = StringField()
    amount = FloatField()
    remainingSeat = IntField()
