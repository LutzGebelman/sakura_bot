import requests
import random
import json
class GiphyApi:
    def __init__(self) -> None:
        self._session = requests.session()
        config = json.loads(open("config.json").read())
        self._api_key = config["credentials"]["giphy_api_key"]
        self._trending_url = "https://api.giphy.com/v1/gifs/trending"
        self._search_url = "https://api.giphy.com/v1/gifs/search"
    
    def search(self, request: str) -> dict:
        offset = random.randint(0, 4999)
        params = {
            'api_key': self._api_key,
            'q': request,
            'offset': offset,
            'limit': 1
        }
        resp = self._session.get(self._search_url, params=params)
        return resp.json()["data"][0]["url"]