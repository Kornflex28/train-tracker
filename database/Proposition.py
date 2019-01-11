from mongoengine import *


class Proposition(Document):
    type = StringField()
    amount = FloatField()
    remainingSeat = IntField()


class Propositions(Document):
    recordedTime = DateTimeField()
    content = ListField(ReferenceField(
        Proposition, reverse_delete_rule=DO_NOTHING))
