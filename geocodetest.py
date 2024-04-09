import googlemaps
import key

gmaps = googlemaps.Client(key= key.key)

query = gmaps.geocode("2253 fairfax rd columbus oh 43221")

location = query[0]['geometry']['location']

lat = location["lat"]
lon = location["lng"]


print(str(lat) + " " + str(lon))