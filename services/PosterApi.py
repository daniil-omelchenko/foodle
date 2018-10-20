import requests

class PosterApi:
    BASE_URL = 'https://omelchenko.joinposter.com/api'
    TOKEN = '018634:9518914b27fda1f0603d229373a5f36a'

    def getMenu(self):
        menu = requests.get(PosterApi.BASE_URL)