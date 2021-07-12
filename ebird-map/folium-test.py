import folium
import csv

m = folium.Map(location=[40.350113, -74.431602])

locationMap = {}

with open('coords.csv', newline='') as csvfile: 
    #reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['Location'] not in locationMap:
            locationMap[row['Location']] = {"species":[{"name":row['Species'], "date":row['Date']}], "coords":row['Coords']}
        else:
            locationMap[row['Location']]["species"].append({"name":row['Species'], "date":row['Date']})



for key in locationMap:
    print(key, len(locationMap[key]['species']))
    coordList = locationMap[key]['coords'].split(',')
    folium.Marker([float(coordList[0]), float(coordList[1])], popup=locationMap[key]['species']).add_to(m)


m.save("index.html")
