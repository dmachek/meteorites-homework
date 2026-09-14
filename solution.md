# Meteorite Landings — Solution

**Author:** Ibrahim Wannous  
**Dataset:** https://dmachek.github.io/meteorites-homework/meteorite_landings.json

---

## Results

| Question | Answer |
|---|---|
| Total entries | 1000 |
| Most massive meteorite | Sikhote-Alin — 23,000,000 g |
| Most frequent year | 1933 (16 meteorites) |

---

## How I Got the Results

### Step 1 Explored the data first
Before writing any code I opened the dataset URL in the browser to understand the structure:
- The data is a JSON array of 1000 objects
- `mass` is stored as a **string** not a number — requires conversion to float
- `year` is stored as a full ISO datetime `"1880-01-01T00:00:00.000"` — I extract only the first 4 characters
- Some entries have **missing** `mass` or `year` fields — handled with `m.get()` to skip them safely

### Step 2 First attempt (failed)
My first solution used Python's built-in `urllib` library but failed with an SSL certificate error caused by a corporate certificate on my machine intercepting HTTPS connections.

### Step 3 Final approach
I read the dataset from the local file already in the repo under `docs/meteorite_landings.json` — this avoids any network or SSL issues entirely and has no external dependencies.

---

## Solution Code

```python
import json
from collections import Counter

with open("docs/meteorite_landings.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# 1. How many entries?
print(f"Total entries: {len(data)}")

# 2. Most massive meteorite
# mass is a STRING in the data
# some entries have no mass at all, so we skip those
with_mass = [(m["name"], float(m["mass"])) for m in data if m.get("mass")]
heaviest = max(with_mass, key=lambda x: x[1])
print(f"Most massive: {heaviest[0]} — {heaviest[1]:,.0f} g")

# 3. Most frequent year
# year looks like "1969-01-01T00:00:00.000" so we take only first 4 characters
years = [m["year"][:4] for m in data if m.get("year")]
top_year, count = Counter(years).most_common(1)[0]
print(f"Most frequent year: {top_year} ({count} meteorites)")
```

---

## Key observations about the data

- `mass` is a string — must convert to float before comparing
- `year` is a full ISO datetime — extracted only the year part
- Some entries have no mass or year — skipped safely using `m.get()`

---

## Bonus — Cloud Deployment

I went beyond the task and built a full cloud deployment:

- **Flask web app** :displays results as a webpage with a searchable table of all 1000 meteorites and a data quality report
- **Docker** :containerized the app so it runs consistently anywhere
- **Terraform** :provisioned all Azure infrastructure as code
- **GitHub Actions** : CI/CD pipeline that automatically builds and deploys on every push
 
**DevOps repo:** https://github.com/ibrahimWanous/meteorites-devops