import os
import sys
import requests
import configparser
import argparse
import logging

logging.basicConfig(filename='../../log.log',
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    level=logging.INFO,
                    datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger(__name__)

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


def request_data(location: str):
    """
    Request weather data from RapidAPI
    :param location: the location want to acquire
    :return: data dump in JSON format
    """
    url = "https://weatherapi-com.p.rapidapi.com/current.json"

    querystring = {"q": location}

    headers = {
        'x-rapidapi-key': config.get('weather-api', 'API_KEY'),
        'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
    }

    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code != 200:
            logger.error(response.json()['error']['message'])
            sys.exit(response.text)
            
        filepath = f"data/{response.json()['location']['name']}/"
        filename = f"updated_at_{response.json()['current']['last_updated_epoch']}.json"

        with open(os.path.join(filepath, filename), 'wb') as f:
            f.write(response.content)
        print(response.text)
    except Exception as e:
        return e


if __name__ == "__main__":
    request_data(args.query)