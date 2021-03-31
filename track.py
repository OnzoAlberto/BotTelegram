import urllib.request
import json
import requests
import os

def func_1():
    print('a')
    return 'si volaaaa'


def from_dhl(code):
    headers = {
        'accept': 'application/json',
        'DHL-API-Key': os.environ.get('DHLkey'),
    }
    params = (
        ('trackingNumber', code),
        ('language', 'en'),
        ('limit', '5'),
    )
    response = requests.get('https://api-eu.dhl.com/track/shipments', headers=headers, params=params)
    order = response.json()['shipments'][0]['events'][1]
    return 'status: ' + order['status'].lower() + '\n' + 'current location: ' + order['location']['address']['addressLocality'] + '\n' + 'last update: ' + order['timestamp'] + '\n'

def download_from_url():
    url = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati"
    italy_list = []
    try:
        with urllib.request.urlopen(url + '/vaccini-summary-latest.json') as response:
            region_list = json.loads(response.read())
            for region in region_list['data']:
                italy_list.append(region)
        return italy_list
    except ValueError:
        print("URL form is invalid")
        print("Ex: http://www.google.com")
        return -1
