import googlemaps
import csv

#look there might be a better way to obbuscate my api key from github, but i am a mere idiot merchant in wont of a wife
import key

gmaps = googlemaps.Client(key= key.key)
list = []

with open("addresses.csv", "r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        list.append(row)
        row["lat"] = 0
        row["lon"] = 0



for store in list[5:100]:
    query = gmaps.geocode(store["ADDRESS"] + store["CITY"] + store["STATE"] + store["ZIP"])

    location = query[0]['geometry']['location']

    store["lat"] = location["lat"]
    store["lon"] = location["lng"]


print(list)

#write results file        
with open("addresses.csv", "w", newline='') as file:
    writer = csv.DictWriter(file, list[0].keys())
    writer.writeheader()
    for row in list:
        writer.writerow(row)