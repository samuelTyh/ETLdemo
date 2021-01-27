import os
import requests
import configparser
import argparse

# Load config file
config = configparser.ConfigParser()
config.read('config.cfg')

parser = argparse.ArgumentParser()
parser.add_argument("query", type=str,
                    help="Query parameter based on which data is sent back. It could be following: \
                    Latitude and Longitude (Decimal degree) e.g: q=48.8567,2.3508 \
                    city name e.g.: q=Paris \
                    US zip e.g.: q=10001 \
                    UK postcode e.g: q=SW1 \
                    Canada postal code e.g: q=G2J \
                    metar: e.g: q=metar:EGLL \
                    iata: e.g: q=iata:DXB \
                    auto:ip IP lookup e.g: q=auto:ip \
                    IP address (IPv4 and IPv6 supported) e.g: q=100.0.0.1")
args = parser.parse_args()


url = "https://weatherapi-com.p.rapidapi.com/current.json"

querystring = {"q": args.query}

headers = {
    'x-rapidapi-key': config.get('weather-api', 'API_KEY'),
    'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
filepath = f"data/{response.json()['location']['name']}/"
filename = f"updated_at_{response.json()['current']['last_updated_epoch']}.json"

with open(os.path.join(filepath, filename), 'wb') as f:
    f.write(response.content)
print(response.text)