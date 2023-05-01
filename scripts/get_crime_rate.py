import json
import pandas
import re

def split_string_by_spaces(input_string):
    p = re.split(r'[ -]', input_string) # split by space and dash
    not_count=['park','east','west','south','north','hill','slope']
    result = [item for item in p if item not in not_count]  # remove the words that are not counted
    return result


def get_population():
    n_population = pandas.read_csv('./datasets/population.csv')
    n_population = n_population[:196]
    population_sheet = n_population[['NTA Name', 'Population']]

    pop_neighborhood = {}
    with open('../fixtures/neighborhood.json', 'r', encoding='utf8') as jf:
        data = json.load(jf)
        listd = {}
        for item in data:
            if item['fields']['name'].lower() not in listd:
                listd[item['fields']['name'].lower()] = item['fields']['name'].lower()

    not_include = []
    listd = list(listd.keys())
    for index, spots in population_sheet.iterrows():
        s = spots['NTA Name'].lower()
        slist = split_string_by_spaces(s)   #get all possible names
        slist.append(s)
        is_in = 0
        for p in listd:
            for i in slist:
                if i in p:  # if the name is in the list
                    is_in = 1
                    if p not in pop_neighborhood:
                        pop_neighborhood[p] = spots['Population']
                    else:
                        pop_neighborhood[p] += spots['Population'] # to solve something like: park south and park north, merge them together
                    break
        if is_in == 0:
            not_include.append(s)
    return pop_neighborhood

def get_result():
    pop_neighborhood = get_population()
    with open("./datasets/crime_rates", "r") as f:
        crime_data = json.load(f)
        with open('../fixtures/neighborhood.json', 'r', encoding='utf8') as jf:
            data= json.load(jf)
            '''
            # first we would like to merge population data with neighborhood data
            # '''
            for item in data:
                if item['fields']['name'].lower() in pop_neighborhood.keys():
                    item['fields']['population'] = pop_neighborhood[item['fields']['name'].lower()]
                else:
                    item['fields']['population'] = None

            for item in data:
                if item["fields"]["name"] in crime_data.keys():
                    item["fields"]["crime_case"] = crime_data[item["fields"]["name"]]   #add number of crime cases

                    if item['fields']['population'] is not None:
                        item["fields"]["crime_rate"] = crime_data[item["fields"]["name"]]/item['fields']['population']  # add crime rate
                    else:
                        item["fields"]["crime_rate"] = None
                else:
                    item["fields"]["crime_rate"] = 0
                    item["fields"]["crime_case"] = 0
            print(data)
            data_list = list(data)
            with open('../fixtures/crime_rate.json', 'w') as ref:
                json.dump(data_list, ref, indent=4)
if __name__ == '__main__':
    get_result()
