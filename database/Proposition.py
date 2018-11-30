from mongoengine import *


class Proposition(Document):
    amount = FloatField()
    remainingSeat = IntField()
