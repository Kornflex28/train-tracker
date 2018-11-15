import json

import requests
import sys


def getGares(searchTerm):
    headers = {
        'Pragma': 'no-cache',
        'Origin': 'https://www.oui.sncf',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'Accept': '*/*',
        'Referer': 'https://www.oui.sncf/',
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
    }
    params = (
        ('userCountry', 'fr-FR'),
        ('searchField', 'origin'),
        ('searchTerm', searchTerm),
    )
    response = requests.get('https://booking.oui.sncf/widget/autocomplete-d2d', headers=headers, params=params)
    return response.json()


alphabet = 'abcdefghijklmnopqrstuvwxyz'
L = []
for x in alphabet:
    for y in alphabet:
        searchTerm = x + y
        try:
            L += getGares(searchTerm)
        except:
            print("error: " + searchTerm)

with open('station.json', 'w') as f:
    json.dump(L, f, ensure_ascii=False)