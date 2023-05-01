import pandas
import json
from geopy.distance import distance
from tqdm import tqdm
global start_point
global end_point

def get_neighborhood():
    with open('./datasets/Neighborhood Names GIS.geojson', 'r', encoding='utf8') as goe_file:
        data = json.load(goe_file)['features']
        return data

def load_crime_data(start_point, end_point):
    data = pandas.read_csv('./datasets/NYPD_Complaint_Data_Current__Year_To_Date_.csv')
    crime_sheet = data[start_point:end_point]
    new_crime_sheet = crime_sheet[['Latitude', 'Longitude']]
    return new_crime_sheet

def get_crime_statistic(crime_sheet,neighborhoods_raw):
    neighborhoods = neighborhoods_raw
    crime_spots = crime_sheet
    frequency = {}
    for index, spots in tqdm(crime_spots.iterrows(), total=crime_spots.shape[0], desc="Processing crime spots"):
        spot_coordinate = (spots['Latitude'], spots['Longitude'])
        nearest_neighborhood = None
        nearest_distance = float('inf')
        spot_coordinate = (spots['Latitude'], spots['Longitude'])
        nearest_neighborhood = None
        nearest_distance = float('inf')
        try:
            for item in neighborhoods:
                neighborhood = item['properties']['name']
                nei_coordinate = (item['geometry']['coordinates'][1], item['geometry']['coordinates'][0])
                dist = distance(nei_coordinate, spot_coordinate).miles

                if dist < nearest_distance:
                    nearest_distance = dist
                    nearest_neighborhood = neighborhood
            if nearest_neighborhood is not None and nearest_neighborhood in frequency.keys():
                frequency[nearest_neighborhood] += 1
            elif nearest_neighborhood is not None and nearest_neighborhood not in frequency.keys():
                frequency[nearest_neighborhood] = 1
        except:
            continue
    print("frequency is: ", frequency)
    result = list(frequency.keys())
    print(len(result))
    return frequency


if __name__ == '__main__':
    crime_sheet = load_crime_data(0,100000)
    neighboorhoods = get_neighborhood()
    frequency = get_crime_statistic(crime_sheet,neighboorhoods)
    with open('crime_rates', 'w') as f:
        json.dump(frequency, f)