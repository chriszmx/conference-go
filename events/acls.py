import json
import requests
from .keys import PEXELS_API_KEY, OPEN_WEATHER_API_KEY


def get_photo(city, state):
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "per_page": 1,
        "query": city + " " + state,
    }
    url = "https://api.pexels.com/v1/search"
    response = requests.get(url, params=params, headers=headers)
    content = json.loads(response.content)
    return {"picture_url": content["photos"][0]["src"]["original"]}


def get_weather_date(city, state):
    headers = {"Authorization": OPEN_WEATHER_API_KEY}
    params = {
        "q": [city, state],
        "appid": OPEN_WEATHER_API_KEY
    }
    url = "https://api.openweathermap.org/data/2.5/weather?q=London&appid={OPEN_WEATHER_API_KEY}"
