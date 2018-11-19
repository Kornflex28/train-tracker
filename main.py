###
from date import DateTime
from station import Station
from travel import Travel


def get_train_data(train):
    train_data={}
    # train numbers
    train_data["numbers"]=[]
    for data in train["segments"] :
        train_data["numbers"].append(data["trainNumber"])
    # train type
    train_data["type"]=train["transporters"]
    # train_data
    train_data["origin_code"]=train["segments"][0]["originStationCode"]
    train_data["destination_code"]=train["segments"][-1]["destinationStationCode"]
    # train date
    train_data["departureDate"]=DateTime.tdate_to_date(train['departureDate'])
    train_data["arrivalDate"]=DateTime.tdate_to_date(train['arrivalDate'])
    # train duration
    train_data["minuteDuration"]=train['minuteDuration']
    # train prices
    train_data["prices"]=[]
    for offer in train["priceProposals"]:
        price = offer["amount"]
        remaining = offer["remainingSeat"]
        train_data["prices"].append((price, remaining))
    return train_data


# return a toString of train data
def train_to_string(train_data):
    duration = str(train_data["minuteDuration"]//60) +"h"+str(train_data["minuteDuration"]%60)
    string = "Train ("+",".join(train_data["type"])+") numero "+",".join(train_data["numbers"])+":\n"+"Depart de "+Station.get_name_by_code(train_data["origin_code"])+" : "+train_data["departureDate"]+"\n"+"Arrivee a "+Station.get_name_by_code(train_data["destination_code"])+" : " + train_data["arrivalDate"]+"\n"+"Duree : "+duration+"\n"+"Prix :\n"
    for price in train_data["prices"]:
        string+= str(price[1]) + " restants à "+str(price[0])+"e\n"
    # print(string)
    return string


def get_trains_data(date,origin_name,destination_name):
    print("Getting response...")
    origin_code = Station.get_code_by_name(origin_name)
    destination_code = Station.get_code_by_name(destination_name)
    trains = Travel.search(date, origin_code, destination_code)
    trains_data = []
    for train in trains :
        trains_data.append(get_train_data(train))
    return trains_data


# return a toString of trains data
def trains_to_string(date,origin_name,destination_name):
    data = get_trains_data(date,origin_name,destination_name)
    string=""
    for k in range(len(data)):
        train = data[k]
        string+= train_to_string(train)+"\n"
    print(string.encode("utf-8"))


trains_to_string(DateTime(2018, 12, 5, 7, 0, 0), "Paris (toutes gares intramuros)", "Rennes (Bretagne)")



