import json


with open("../fixtures/neighborhood.json", "r") as f:
    neighborhoods = json.load(f)

with open("../fixtures/crime.json", "r") as f:
    crimes = json.load(f)

print(len(neighborhoods))
print(len(crimes))

consolidated = {}
neighborhood_data = []
for neighborhood in neighborhoods:
    neighborhood_data.append(neighborhood["fields"]["name"])
    consolidated[neighborhood["fields"]["name"]] = {
        "population": 0,
        "crimes": 0,
    }

for crime in crimes:
    name = crime["fields"]["name"]
    if name in consolidated:
        consolidated[name]["population"] = crime["fields"]["population"]
        consolidated[name]["crimes"] = crime["fields"]["crime_case"]


print(len(consolidated))

final = []
for k, v in consolidated.items():
    final.append({
        k: v
    })

print(len(final))
print(len(neighborhood_data))

#     population = consolidated[neighborhood["fields"]["name"]]["population"] if consolidated[neighborhood["fields"]["name"]]["population"] else 0
# TypeError: 'NoneType' object is not subscriptable

filtered = []
for neighborhood in neighborhoods:
    name = neighborhood["fields"]["name"]
    if name in consolidated:
        neighborhood["fields"]["population"] = consolidated[name]["population"]
        neighborhood["fields"]["crimes"] = consolidated[name]["crimes"]
        filtered.append(neighborhood)


with open("../fixtures/neighborhood.json", "w") as f:
    json.dump(filtered, f)
