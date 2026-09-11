import json

# Martino @2026
# feel free to use or edit this script ;)

# Input JSON file
with open("meteorite_landings.json", "r", encoding="utf-8") as file:
    data = json.load(file)


# 1. How many entries are in the dataset?
print("Number of entries:", len(data))


# 2. What is the name and mass of the most massive meteorite in this dataset?
heaviest = None

for meteorite in data:
    mass = meteorite.get("mass")

    if mass:
        if heaviest is None or float(mass) > float(heaviest["mass"]):
            heaviest = meteorite

print("The heaviest meteorite:", heaviest["name"])
print("Mass:", heaviest["mass"], "g")


# 3. What is the most frequent year in this dataset?
years = {}

for meteorite in data:
    year = meteorite.get("year")

    if year:
        year = year[:4]

        if year in years:
            years[year] += 1
        else:
            years[year] = 1

most_common_year = max(years, key=years.get)

print("The most frequent year:", most_common_year)
print("occurrence count:", years[most_common_year])
