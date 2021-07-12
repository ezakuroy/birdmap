import folium
import requests
import os.path
import urllib.request
from threading import Thread

def localSpecies(mode, speciesName, lat, lng, distance):

    if lat is None:
    	lat = 40.72

    if lng is None:
    	lng = -74.04

    if distance is None:
        distance = 25

    #m = folium.Map(location=[lat, lng])
    url ='https://api.ebird.org/v2/data/obs/geo/recent/'
    if mode == 'species':
        url += speciesName
        back = 7
        maxResults = 100
    elif mode == 'notable':
        url += 'notable'
        back = 7
        maxResults = 100
    elif mode == 'recent':
        back = 7
        maxResults = 100
    
    url += '?lat=' + str(lat) + '&lng=' + str(lng) + '&back=' + str(back) + '&maxResults=' + str(maxResults)
    print('url: ' + url)

    headers = {'X-eBirdApiToken' : '8qd6qep4lsli'}

    response = requests.get(url, headers=headers)

    print(response)

    thread = Thread(target=downloadImages, kwargs={'data': response.json()}).start()

    #data = response.json()

    #for sighting in data:
        #popup = "<h3>" + sighting["locName"] + "</h3></br>" + sighting["obsDt"]
        #if "howMany" in sighting:
        #    popup += " - " + str(sighting["howMany"])

        #if "subId" in sighting:
        #    popup += " - <a target='_blank' href='https://ebird.org/checklist/" + sighting["subId"] + "'>Checklist" + sighting["subId"] + "</a>"

        #folium.Marker([round(sighting["lat"], 2), round(sighting["lng"], 2)], popup=popup).add_to(m)
        

    #return m._repr_html_()
    #return str(response.json())

    return response.json()


def downloadImages(data):


    print(data)

    speciesSet = set()
    for sighting in data:
        speciesSet.add(sighting["speciesCode"])

    noFileSet = set()

    for bird in speciesSet:
        if os.path.isfile('../ebird-map-js/static/images/image-' + bird + '.png') is False:
            noFileSet.add(bird)
        else:
            print('Already found ' + bird)

    print(noFileSet)

    for bird in noFileSet:
        macUrl = 'https://search.macaulaylibrary.org/catalog.json?searchField=species&taxonCode=' + bird + '&hotspotCode=&regionCode=&customRegionCode=&userId=&_mediaType=on&mediaType=p&species=&region=&hotspot=&customRegion=&mr=M1TO12&bmo=1&emo=12&yr=YALL&by=1900&ey=2021&user=&view=Gallery&sort=rating_rank_desc&_req=on&cap=no&subId=&catId=&_spec=on&specId=&collection=&collectionCatalogId=&dsu=-1&start=0&_=1626045648995&limit=1'
        response = requests.get(macUrl)
        macData = response.json()

        if macData["results"] is not None:
            if macData["results"]["content"] is not None:
                print('Downloading ' + bird)
                urllib.request.urlretrieve(macData["results"]["content"][0]["previewUrl"], '../ebird-map-js/static/images/image-' + bird + '.png')  


