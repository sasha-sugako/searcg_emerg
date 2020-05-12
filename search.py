import sys
from io import BytesIO
import requests
from PIL import Image
from find_spn import spn_func
from geo import get_distance

toponym_to_find = sys.argv[1:]
geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
geocoder_params = {
    "apikey": "",
    "geocode": toponym_to_find,
    "format": "json"}
response = requests.get(geocoder_api_server, params=geocoder_params)
if not response:
    pass
json_response = response.json()
toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
toponym_coodrinates = toponym["Point"]["pos"]
toponym_longitude, toponym_lattitude = toponym_coodrinates.split(" ")
search_api_server = "https://search-maps.yandex.ru/v1/"

search_params = {
    "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
    "text": "аптека",
    "lang": "ru_RU",
    "ll": toponym_longitude + ',' + toponym_lattitude,
    "type": "biz"
}
response = requests.get(search_api_server, params=search_params)
if not response:
    pass
json_response = response.json()
organization = json_response["features"][0]
org_name = organization["properties"]["CompanyMetaData"]["name"]
org_address = organization["properties"]["CompanyMetaData"]["address"]
point = organization["geometry"]["coordinates"]
org_point = "{0},{1}".format(point[0], point[1])
coord_top = "{0},{1}".format(toponym_longitude, toponym_lattitude)
map_params = {
    "ll": toponym_longitude + ',' + toponym_lattitude,
    "spn": ",".join(spn_func(coord_top, org_point)),
    "l": "map",
    "pt": "{0},pm2dgl~{1},pm2dgl".format(org_point, coord_top)
}
map_api_server = "http://static-maps.yandex.ru/1.x/"
response = requests.get(map_api_server, params=map_params)
Image.open(BytesIO(
    response.content)).show()
print(org_name)
print(org_address)
print(organization["properties"]["CompanyMetaData"]['Hours']['text'])
print(get_distance([float(point[0]), float(point[1])], [float(toponym_longitude), float(toponym_lattitude)]), 'м')