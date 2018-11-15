###
import requests
import datetime as dt

sncfURL = 'https://www.oui.sncf/proposition/rest/search-travels/outward'

#need to find database
towns = {"Paris" : {"code":"FRPAR","name":"Paris (Toutes gares intramuros)"},"Brest":{"code":"FRBES","name":"Brest"},"Lyon":{"code":"FRLYS","name":"Lyon (Toutes gares intramuros)"},"Marseille":{"code":"FRMRS","name":"Marseille (Toutes gares)"},"Naucelle":{"code":"FRFWF","name":"Naucelle"},"Toulouse":{"code":"FRTLS","name":"Toulouse (Toutes gares)"},"Rennes":{"code":"FRRNS","name":"Rennes"},"Montpellier":{"code":"FRMPT","name":"Montpellier (toutes gares)"}}


### Useful Fonctions

#return string format for the Request
#date = datetime
def conv_TDate(date):
    return str(date)[:10]+"T"+str(date)[11:19]
    
#return date in string
def conv_Date(tdate):
    return tdate[:10]+" "+tdate[11:19]
    
#Return the data for the request
#startLocation : string
#endLocation : string
#date = datetime
def createReqData(date,startLocation,destinationLocation):
    originCode = towns[startLocation]["code"]
    originName = towns[startLocation]["name"]
    destinationCode = towns[destinationLocation]["code"]
    destinationName = towns[destinationLocation]["name"]
    
    tdate = conv_TDate(date)
    
    data = '{"origin":"'+originName+'","originCode":"'+originCode+'","originLocation":{"id":null,"label":null,"longitude":null,"latitude":null,"type":"G","country":null,"stationCode":"'+originCode+'","stationLabel":null},"destination":"'+destinationName+'","destinationCode":"'+destinationCode+'","destinationLocation":{"id":null,"label":null,"longitude":null,"latitude":null,"type":"G","country":null,"stationCode":"'+destinationCode+'","stationLabel":null},"via":null,"viaCode":null,"viaLocation":null,"directTravel":false,"asymmetrical":false,"professional":false,"customerAccount":false,"oneWayTravel":true,"departureDate":"'+tdate+'","returnDate":null,"travelClass":"SECOND","country":"FR","language":"fr","busBestPriceOperator":null,"passengers":[{"travelerId":null,"profile":"YOUNG","age":null,"birthDate":null,"fidelityCardType":"NONE","fidelityCardNumber":null,"commercialCardNumber":"","commercialCardType":"YOUNGS","promoCode":null,"lastName":null,"firstName":null,"phoneNumer":null,"hanInformation":null}],"animals":[],"bike":"NONE","withRecliningSeat":false,"physicalSpace":null,"fares":[],"withBestPrices":false,"highlightedTravel":null,"nextOrPrevious":false,"source":"FORM_SUBMIT","targetPrice":null,"han":false,"outwardScheduleType":"BY_DEPARTURE_DATE","inwardScheduleType":"BY_DEPARTURE_DATE","currency":null,"codeFce":null,"companions":[],"asymetricalItinerary":{}}'
    
    return data
    
def query(date,startLocation,endLocation):
    headers = {'Content-Type': 'application/json',}
    data = createReqData(date,startLocation,endLocation)
    response = requests.post(sncfURL, headers=headers, data=data)
    return response
    


def getTrainData(train):
    trainData={}
    #train numbers
    trainData["numbers"]=[]
    for data in train["segments"] :
        trainData["numbers"].append(data["trainNumber"])
    #train type
    trainData["type"]=train["transporters"]
    #train stations
    trainData["originCode"]=train["segments"][0]["originStationCode"]
    trainData["destinationCode"]=train["segments"][-1]["destinationStationCode"]
    #train date
    trainData["departureDate"]=conv_Date(train['departureDate'])
    trainData["arrivalDate"]=conv_Date(train['arrivalDate'])
    #train duration
    trainData["minuteDuration"]=train['minuteDuration']
    #train prices
    trainData["prices"]=[]
    for offer in train["priceProposals"] :
        price = offer["amount"]
        remaining = offer["remainingSeat"]
        trainData["prices"].append((price,remaining))
    
    return trainData
    
#return a toString of train data
def train_String(trainData):
    duration = str(trainData["minuteDuration"]//60) +"h"+str(trainData["minuteDuration"]%60)
    string = "Train ("+",".join(trainData["type"])+") numero "+",".join(trainData["numbers"])+":\n"+"Depart de "+trainData["originCode"]+" : "+trainData["departureDate"]+"\n"+"Arrivee a "+trainData["destinationCode"]+" : " + trainData["arrivalDate"]+"\n"+"Duree : "+duration+"\n"+"Prix :\n"
    for price in trainData["prices"]:
        string+= str(price[1]) + " restants à "+str(price[0])+"e\n"
    #print(string)
    return string
    
    
def getTrainsData(response):
    trains = response.json()["trainProposals"]
    trainsData = []
    for train in trains :
        trainsData.append(getTrainData(train))
    return trainsData

#return a toString of trains data
def trains_String(response):
    data = getTrainsData(response)
    string=""
    for k in range(len(data)):
        train = data[k]
        string+= train_String(train)+"\n"
    print(string)
        

    