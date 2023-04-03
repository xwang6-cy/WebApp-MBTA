# Your API KEYS (you need to use your own keys - very long random characters)
#from config import MAPBOX_TOKEN, MBTA_API_KEY


# Useful URLs (you need to add the appropriate parameters for your requests)
MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
MBTA_BASE_URL = "https://api-v3.mbta.com/stops"


# A little bit of scaffolding if you want to use it

import urllib.parse
import requests
from pprint import pprint




MAPBOX_API_KEY = "pk.eyJ1IjoiamRpbmcyIiwiYSI6ImNsZnpycTR1aTEwNHozZG1rNzc0eGRsaGUifQ.TXqxolgtqCTPJk3kbB_bQw"
MBTA_API_kEY= 'f28ffef47e91409785f061cb7caf1873'

def get_json(url: str) -> dict:
    """
    Given a properly formatted URL for a JSON web API request, return a Python JSON object containing the response to that request.

    Both get_lat_long() and get_nearest_station() might need to use this function.
    """
    response = requests.get(url)
    data = response.json()
    return data

def get_lat_long(place_name: str) -> tuple[str, str]:
    """
    Given a place name or address, return a (latitude, longitude) tuple with the coordinates of the given place.

    See https://docs.mapbox.com/api/search/geocoding/ for Mapbox Geocoding API URL formatting requirements.
    """
    MAPBOX_BASE_URL = "https://api.mapbox.com/geocoding/v5/mapbox.places"
    MAPBOX_TOKEN = "pk.eyJ1IjoiamRpbmcyIiwiYSI6ImNsZnpycTR1aTEwNHozZG1rNzc0eGRsaGUifQ.TXqxolgtqCTPJk3kbB_bQw"
    query = urllib.parse.quote_plus(place_name)
    url = f"{MAPBOX_BASE_URL}/{query}.json?access_token={MAPBOX_TOKEN}&types=poi"

    data = get_json(url)
    if "features" not in data:
        return None, None
    longitude, latitude = data["features"][0]["center"]
    return latitude, longitude

    

    data = get_json(url)
    longitude, latitude = data["features"][0]["center"]
    return latitude, longitude

def get_nearest_station(latitude: str, longitude: str) -> tuple[str, bool]:
    """
    Given latitude and longitude strings, return a (station_name, wheelchair_accessible) tuple for the nearest MBTA station to the given coordinates.

    See https://api-v3.mbta.com/docs/swagger/index.html#/Stop/ApiWeb_StopController_index for URL formatting requirements for the 'GET /stops' API.
    """
    url = f"https://api-v3.mbta.com/stops?sort=distance&filter[latitude]={latitude}&filter[longitude]={longitude}&api_key={'f28ffef47e91409785f061cb7caf1873'}"

    data = get_json(url)
    
    if not data["data"]:
        return None, None
    
    stop_name = data["data"][0]["attributes"]["name"]
    wheelchair_accessible = data["data"][0]["attributes"]["wheelchair_boarding"] == 1
    return stop_name, wheelchair_accessible


def find_stop_near(place_name: str) -> tuple[str, bool]:
    """
    Given a place name or address, return the nearest MBTA stop and whether it is wheelchair accessible.

    This function might use all the functions above.
    """
    # Get the latitude and longitude coordinates for the given place
    latitude, longitude = get_lat_long(place_name)
    
    # If no coordinates were found, return None
    if latitude is None or longitude is None:
        return None
    
    # Find the nearest MBTA station to the given coordinates
    station_name, wheelchair_accessible = get_nearest_station(latitude, longitude)
    
    return station_name, wheelchair_accessible




def main():
    """
    You can test all the functions here
    """
    place_name = "Babson College"
    station_name, wheelchair_accessible = find_stop_near(place_name)
    if station_name is None:
        print(f"No MBTA stop was found near {place_name}.")
    else:
        print(f"The nearest MBTA stop to {place_name} is {station_name}.")
        print(f"It is{' ' if wheelchair_accessible else ' not '}wheelchair accessible.")

if __name__ == '__main__':
    main()
