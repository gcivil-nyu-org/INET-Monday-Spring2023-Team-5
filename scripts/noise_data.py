import json
import numpy as np
import re


def open_source_data():
    with open('../static/data/tabulation-v2.geojson', 'r') as f:
        data = json.load(f)
        return data

def open_raw_data():
    with open('../fixtures/neighborhood.json','r') as fn:
        data = json.load(fn)
        return data

def calculate_crime_rate(data):
    hightest_noise_rate = 0
    for item in data:
        if 'noise_count' in  item['fields']:
            noise_rate = item['fields']['noise_count']
            if noise_rate > hightest_noise_rate:
                hightest_noise_rate = noise_rate

    percentages = np.array([20, 40, 60, 80, 100])
    results = [(hightest_noise_rate * p) / 100 for p in percentages]
    return results


def split_string_by_spaces(input_string):
    p = re.split(r'[ -]', input_string)  # split by space and dash
    not_count = ['park', 'east', 'west', 'south', 'north', 'hill', 'slope']
    result = [item for item in p if item not in not_count]
    result.insert(0, input_string)  # remove the words that are not counted
    return result


def match(neigh, geojson,rate_standard):
    for item in geojson['features']:
        item['properties']['noise_rate'] = 0
        names = split_string_by_spaces(item['properties']['ntaname'])
        for name in names:
            for n in neigh:
                if name in n['fields']['name'] and 'noise_count' in n['fields']:
                    noise_rate = n['fields']['noise_count']
                    for p in range(len(rate_standard)):
                        if noise_rate <= rate_standard[p]:
                            item['properties']['noise_rate'] = p+1
                            break
                    break
                else:
                    item['properties']['noise_rate'] = 0
    print(geojson)
    return geojson

if __name__ == '__main__':
    source_data = open_source_data()
    raw_data = open_raw_data()
    rate_standard = calculate_crime_rate(raw_data)
    result = match(raw_data, source_data,rate_standard)
    with open('../static/data/tabulation-v2.geojson', 'w') as f:
        json.dump(result, f,indent=2)
