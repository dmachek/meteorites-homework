# Meteorite Landings Analysis - Methodology

## Overview

This document describes the methodology for analyzing Earth meteorite landings data to answer the three required questions.

---

## Data Source

- **URL:** https://dmachek.github.io/meteorites-homework/meteorite_landings.json
- **Format:** JSON array of meteorite records
- **Access Method:** HTTP GET request with validation (10-second timeout)

---

## Research Questions & Methodology

### Question 1: How many entries are in the dataset?

#### Objective
Determine the total number of meteorite landing records in the dataset.

#### Methodology
```python
entry_count = len(data)
```

**Process:**
1. Fetch the complete JSON array from the remote URL
2. Parse JSON response into a Python list
3. Use `len()` to count array elements
4. Return the raw count without filtering

---

### Question 2: What is the name and mass of the most massive meteorite?

#### Objective
Identify the meteorite with the largest recorded mass and retrieve its name.

#### Methodology

**Step 1: Parse Mass Values**
```python
def parse_mass(value):
    if value is None or value == "":
        return None
    try:
        mass = float(value)
    except (ValueError, TypeError):
        return None
    return mass if math.isfinite(mass) else None
```

**Step 2: Find Maximum**
```python
valid_entries = [(name, mass), ...]
name, mass = max(valid_entries, key=lambda item: (item[1], item[0].lower()))
```

**Process:**
1. Filter entries where 'mass' field exists and is not empty
2. Convert mass strings to float for numeric comparison
3. Apply max() function with numeric key
4. Extract name and mass from result

**Data Validation:**
- Exclude entries without mass data
- Skip empty or non-numeric values
- Convert to numeric type for proper comparison
- Use a deterministic tie-breaker (name)

**Mass Unit:** Grams (converted to kg for display: mass_kg = mass_grams / 1000)

---

### Question 3: What is the most frequent year in this dataset?

#### Objective
Determine which year has the most recorded meteorite landings.

#### Methodology

**Step 1: Extract and Validate Years**
```python
def parse_year(value):
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return int(value)
    if isinstance(value, str):
        match = re.match(r"\\s*(\\d{4})", value)
        return int(match.group(1)) if match else None
```

**Step 2: Count Frequencies**
```python
from collections import Counter
year_counts = Counter(years)
max_count = max(year_counts.values())
most_frequent_year = min(year for year, count in year_counts.items() if count == max_count)
```

**Process:**
1. Extract 'year' field from all entries
2. Validate year format (convert to integer, skip non-positive values)
3. Use Counter to count occurrences
4. Retrieve year with highest count (earliest year on tie)

**Data Validation:**
- Exclude missing or empty year fields
- Accept integer or ISO 8601-style strings
- Skip malformed entries
- O(n) time complexity

---

## Error Handling Strategy

### Network Errors
```python
except urllib.error.URLError as e:
    print(f"Connection error: {e.reason}")
    raise
```

### Data Parsing Errors
```python
except json.JSONDecodeError as e:
    print(f"Invalid JSON response: {e}")
    raise
```

### Type Conversion Errors
```python
mass = parse_mass(entry.get("mass"))
year = parse_year(entry.get("year"))
```

---

## Data Quality Assessment

### Strengths
- ✅ Comprehensive dataset with meteorite records
- ✅ Consistent JSON structure across entries
- ✅ Most records have complete data

### Known Issues Handled
- ⚠️ Some entries missing mass values
- ⚠️ Some entries missing year values
- ⚠️ Non-numeric mass/year values
- ⚠️ Empty string placeholders

### Handling Strategy
- Invalid data is filtered, not used in analysis
- Invalid entries don't stop execution
- Analysis completes with available valid data

---

## Code Structure

### Main Functions

#### `fetch_dataset(url: str) -> List[Dict]`
- Fetches JSON from remote URL
- Validates HTTP response
- Parses and returns data
- Handles network and parsing errors

#### `count_entries(data: List) -> int`
- Counts total records
- Simple operation: `len(data)`
- Displays result

#### `find_most_massive(data: List) -> Tuple[str, float, int]`
- Filters valid mass entries
- Finds maximum mass
- Returns (name, mass, valid_count)

#### `find_most_frequent_year(data: List) -> Tuple[int, int, int]`
- Extracts and validates years
- Counts frequencies
- Returns (year, count, valid_count)

#### `generate_report(...) -> str`
- Creates formatted output report
- Includes methodology
- Documents results
- Saves to file

#### `main() -> int`
- Orchestrates analysis pipeline
- Error handling and logging
- Returns exit code

---

## Execution & Results

### How to Run
```bash
cd analysis
python3 meteorite_analysis.py
```

### Output
- Console: Formatted results with details
- File: `results/analysis_report.txt` - Full report with methodology
- Exit Code: 0 for success, 1 for failure

### Result Format
```
================================================================================
                   EARTH METEORITE LANDINGS ANALYSIS REPORT
================================================================================

Question 1: How many entries are in the dataset?
   ✓ Answer: [NUMBER] entries

Question 2: What is the name and mass of the most massive meteorite?
   ✓ Answer: 
      Name: [NAME]
      Mass: [MASS] grams ([MASS_KG] kg)

Question 3: What is the most frequent year in this dataset?
   ✓ Answer: 
      Year: [YEAR]
      Occurrences: [COUNT] meteorite landings
```

---

## Reproducibility

The solution is fully reproducible:
- ✅ No hardcoded results
- ✅ All values computed from data
- ✅ Documented methodology
- ✅ Source code included
- ✅ Results saved to file
- ✅ Error handling for edge cases

---

## References

- [Meteorite Data Source](https://dmachek.github.io/meteorites-homework/meteorite_landings.json)
- [Python Collections Counter](https://docs.python.org/3/library/collections.html#collections.Counter)
- [JSON Module](https://docs.python.org/3/library/json.html)

---

**Document Version:** 1.0  
**Date:** 2026-02-01  
**Author:** Analysis Team
