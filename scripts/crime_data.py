import json
import numpy as np
import re


def open_source_data():
    with open('../static/data/tabulation.geojson', 'r') as f:
        data = json.load(f)
        return data

def open_raw_data():
    with open('../fixtures/neighborhood.json','r') as fn:
        data = json.load(fn)
        return data

def calculate_crime_rate(data):
    hightest_crime_rate = 0
    for item in data:
        if item['fields']['crimes'] is not None and item['fields'][
            'population'] is not None:  # if we only consider the number of crimes and ignore the population is unfair to some large neighborhoods
            crime_rate = item['fields']['crimes'] / item['fields']['population']
            if crime_rate > hightest_crime_rate:
                hightest_crime_rate = crime_rate

    percentages = np.array([20, 40, 60, 80, 100])
    results = [(hightest_crime_rate * p) / 100 for p in percentages]
    return results


def split_string_by_spaces(input_string):
    p = re.split(r'[ -]', input_string)  # split by space and dash
    not_count = ['park', 'east', 'west', 'south', 'north', 'hill', 'slope']
    result = [item for item in p if item not in not_count]
    result.insert(0, input_string)  # remove the words that are not counted
    return result


def match(neigh, geojson,rate_standard):
    for item in geojson['features']:
        names = split_string_by_spaces(item['properties']['ntaname'])
        for name in names:
            for n in neigh:
                if name in n['fields']['name'] and n['fields']['population'] is not None and n['fields']['crimes'] is not None:
                    crime_rate = n['fields']['crimes'] / n['fields']['population']
                    for p in range(len(rate_standard)):
                        if crime_rate <= rate_standard[p]:
                            item['properties']['crime_rate'] = p+1
                            break
                    break
                else:
                    item['properties']['crime_rate'] = 0
    print(geojson)
    return geojson

if __name__ == '__main__':
    source_data = open_source_data()
    raw_data = open_raw_data()
    rate_standard = calculate_crime_rate(raw_data)
    result = match(raw_data, source_data,rate_standard)
    with open('../static/data/tabulation_new.geojson', 'w') as f:
        json.dump(result, f,indent=2)
