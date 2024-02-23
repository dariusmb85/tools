import requests
from pprint import pprint
url = "https://api.inaturalist.org/v1/observations?geo=true&taxon_id=52775&order=desc&per_page=25&order_by=created_at"
response = requests.get(url=url)
data = response.json()


data['results'][0]['location']


data['results'][1]['location']
