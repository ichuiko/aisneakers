import requests
import json
from datetime import datetime

class Strapp() :
    URL = 'http://194.67.108.143:1337'

    def localShops(self):
        url = f'{url}/local-shops'
        r = requests.get(url)
        data = json.loads(r.text)
        print(data)

a = Strapp()
a.localShops()