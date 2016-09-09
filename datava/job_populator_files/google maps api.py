import googlemaps
from datetime import datetime
import sys
import pandas as pd

data = pd.read_table(r'C:\Users\alsherman\Desktop\Programming\hackathon\joblistings.merged.parsed.unique.grpbyyear.2016.tsv', sep='\t')
data.head()
data.columns

gmaps = googlemaps.Client(key='AIzaSyAb416HhO9hmtIBYR4Zl-zZ3QAF0m7nJGE')

destinations = []

for ind, row in data.iterrows():
    # extract job data
    listed_latitude = row['jobLocation_geo_latitude']
    listed_longitude = row['jobLocation_geo_longitude']
    hiringOrganization = row['hiringOrganization_organizationName']
    jobLocation = row['jobLocation_address_locality']
    
    # geocode job locations using Google Places API
    destination = '{} | {}, VA'.format(hiringOrganization, jobLocation)    
    geocode_result = gmaps.places(query=destination,
                                  location=(listed_latitude, listed_longitude ))    

    
    if ind == 1: 
        sys.exit()
    
    # get Google Place results (e.g. Latitude, Longitude, Place_id)
    results = geocode_result['results'][1]    
    latitude = results['geometry']['location']['lat']
    longitude = results['geometry']['location']['lng']
    place_id = results['place_id']
    types = results['types']
    address = results['formatted_address']

    destinations.append({'title':destination, 'location':{'lat':latitude,'lng':longitude}})
        
    
    # get place information
    gmaps.place(place_id=place_id, 
                language=None)
    
    
    # get information on places nearby
    keywords = ['childcare']
    for keyword in keywords:
        place_of_interest = gmaps.places_nearby(
            location={'lat':latitude,'lng':longitude}, 
            radius=1610, 
            keyword=keyword, 
            language=None, min_price=None, max_price=None, name=None, open_now=False,
            rank_by=None, type=None, page_token=None
        )
    
        for result in place_of_interest['results']:
            lat = result['geometry']['location']['lat']
            lng = result['geometry']['location']['lng']
            name = result['name']
            place_id = result['place_id']
        
        gmaps.place(place_id=place_id, language=None)
        
        
    # get distance
    user_address = '401 12th street south arlington, VA'
    gmaps.distance_matrix(origins=user_address, 
                          destinations={'lat':latitude,'lng':longitude},
                          mode=None, language=None, avoid=None, units=None,
                          departure_time=None, arrival_time=None, transit_mode=None,
                          transit_routing_preference=None, traffic_model=None)









for city in cities:
    destination = 'ABF Freight System, Inc | Richmond, VA'# in {}, {}'.format(city, 'VA')    
    geocode_result = gmaps.places(query=destination, location=(37.55376, -77.46026))
    latitude = geocode_result[0]['geometry']['location']['lat']
    longitude= geocode_result[0]['geometry']['location']['lng']
    destinations.append({'title':destination, 'location':{'lat':latitude,'lng':longitude}})

gmaps.place(place_id='ChIJjUFODXkNsYkRQoO7w1ZMcmw', language=None)

for city in cities:
    destination = 'AAA Motor Club'# in {}, {}'.format(city, 'VA')    
    geocode_result = gmaps.geocode(destination, {'administrative_area': 'VA','country': 'US'})
    latitude = geocode_result[0]['geometry']['location']['lat']
    longitude= geocode_result[0]['geometry']['location']['lng']
    destinations.append({'title':destination, 'location':{'lat':latitude,'lng':longitude}})









### WORK AREA
gmaps = googlemaps.Client(key='AIzaSyAb416HhO9hmtIBYR4Zl-zZ3QAF0m7nJGE')


# Geocoding an address
geocode_result = gmaps.geocode('ABB, Inc. Va south boston')

# Look up an address with reverse geocoding
reverse_geocode_result = gmaps.reverse_geocode((33.1262476, -117.3115765))

# Request directions via public transit
now = datetime.now()
directions_result = gmaps.directions("Sydney Town Hall",
                                     "Parramatta, NSW",
                                     mode="transit",
                                     departure_time=now)

origin = '401 12th street south arlington va 22202'
destination = 'deloitte rosslyn'
distance = gmaps.distance_matrix(origins=origin, destinations=destination,
                        mode='walking', language=None, avoid=None, units='imperial',
                        departure_time=None, arrival_time=None, transit_mode=None,
                        transit_routing_preference=None, traffic_model=None)

geocode_result = gmaps.geocode(destination)
latitude = geocode_result[0]['geometry']['location']['lat']
longitude= geocode_result[0]['geometry']['location']['lng']

places = gmaps.places_nearby(location=(latitude,longitude), radius=None, keyword=None, language=None,
                  min_price=None, max_price=None, name=None, open_now=False,
                  rank_by=None, type=None, page_token=None)
                    

gmaps.places(query='food', location=(latitude, longitude), radius=None, language=None,
           min_price=None, max_price=None, open_now=False, type=None,
           page_token=None)
           
photo = r'CoQBdwAAAHGCckHA3LOhSiwRZnXcT_c7BJDWgCQvnrJhm4-CJyfvsmGsZ4qJA2tRAl-lreCasDbSJ1U4HG0lIGUwtMz67Yi_BJXqLx-8NEVK3lqCIgwFF8K41elNrxzpdyMqprKFzmwaHg0GczA_Cd9mJybnXu5lRKyyEy3ETyM-1ENTk7G9EhCqNZUhVVpjDLsR_q9yo48NGhRuoABrq6LO_dsHsKvLC5SpO8b4Rg'
for i in gmaps.places_photo(photo_reference=photo, max_width=400, max_height=400):
    print i