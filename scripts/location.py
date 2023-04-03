import json
from geopy.distance import distance

def get_neighborhood(lat,lon):
    min_distance = float('inf')
    with open('./datasets/Neighborhood Names GIS.geojson', 'r', encoding='utf8') as goe_file:
        data = json.load(goe_file)['features']
        for item in data:
            neighborhood = item['properties']['name']
            coordinate = item['geometry']['coordinates']
            origin = (lat, lon)
            destination = (coordinate[0], coordinate[1])
            dist = distance(origin, destination).miles
            if dist < min_distance:
                min_distance = dist
                min_neighborhood = neighborhood
        if min_distance > 5:  # if all neighborhoods are more than 5 miles away, then no neighborhood is found
            result='No neighborhood found within 5 miles,please make sure you are in NY'
        else:
            result={'Neighborhood':min_neighborhood, 'distance=':min_distance}
    return result
