import requests
import sys

n = len(sys.argv)
print("Total arguments passed:", n)

species="hoowar"
lat = 40.72
lon = -74.05

if n > 1 and sys.argv[1] is not None:
    species = sys.argv[1]

if  n > 2 and sys.argv[2] is not None:
    lat = round(sys.argv[2], 2)

if n > 3 and sys.argv[3] is not None:
    lon = round(sys.argv[3], 2)


url = 'https://api.ebird.org/v2/data/obs/geo/recent/' + species + '?lat=' + str(lat) + '&lng=' + str(lon)
print('url: ' + url)

headers = {'X-eBirdApiToken' : '8qd6qep4lsli'}

response = requests.get(url, headers=headers)

print(response.text)
