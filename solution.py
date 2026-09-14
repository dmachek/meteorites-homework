import requests
import json
from collections import Counter

with open("docs/meteorite_landings.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 1. How many entries?
print(f"Total entries: {len(data)}")

# 2. Most massive meteorite
# mass is a STRING in the data, so we convert to float
# some entries have no mass at all, so we skip those
with_mass = [(m["name"], float(m["mass"])) for m in data if m.get("mass")]
heaviest = max(with_mass, key=lambda x: x[1])
print(f"Most massive: {heaviest[0]} — {heaviest[1]:,.0f} g")

# 3. Most frequent year
# year looks like "1969-01-01T00:00:00.000" so we take only first 4 characters
years = [m["year"][:4] for m in data if m.get("year")]
top_year, count = Counter(years).most_common(1)[0]
print(f"Most frequent year: {top_year} ({count} meteorites)")