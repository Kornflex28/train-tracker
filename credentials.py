from mongoengine import *

MONGO_IP = "51.77.136.3"
MONGO_USER = "user"
MONGO_PASSWD = "SkRmjsP78YWYRdQT"
MONGO_DB = "train-tracker"

connect(
    db=MONGO_DB,
    username=MONGO_USER,
    password=MONGO_PASSWD,
    host=MONGO_IP
)