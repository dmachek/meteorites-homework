# Earth Meteorite Landings Analysis

## Overview

This solution retrieves and analyzes the JSON dataset provided in the assignment:

```text
https://dmachek.github.io/meteorites-homework/meteorite_landings.json
```

The goal is to answer:

1. How many entries are in the dataset?
2. What is the name and mass of the most massive meteorite?
3. What is the most frequent year?

## Results

| Question | Result |
| --- | --- |
| Number of entries | **1,000** |
| Most massive meteorite | **Sikhote-Alin — 23,000,000 g (23,000 kg)** |
| Most frequent year | **1933 — 16 entries** |

## Initial Inspection

Before implementing the solution, I inspected the provided endpoint using
Postman to understand the JSON structure and available fields.

During the inspection, I noticed that some meteorite records do not contain a
`mass` value. The implementation therefore handles missing or malformed values
instead of assuming that every record is complete.

I also inspected the larger `Meteorite-Landings.json` file included in the
repository. During my inspection, I found that the file could not be parsed as
valid JSON.

For this reason, the solution explicitly handles JSON decoding errors:

```python
try:
    data = response.json()
except requests.exceptions.JSONDecodeError as error:
    raise ValueError("Invalid JSON") from error
```

This ensures that malformed JSON is detected and reported clearly rather than
being processed as valid input.

## Approach

The dataset is retrieved using Python's `requests` library:

```python
response = requests.get(url, timeout=(5, 30))
response.raise_for_status()
data = response.json()
```

The timeout uses:

- a 5-second connection timeout
- a 30-second read timeout

The decoded response is also validated to ensure that the top-level JSON
structure is a list.

### Number of entries

The total number of records is calculated using:

```python
len(meteorites)
```

Result:

```text
1000
```

### Most massive meteorite

The script iterates through each meteorite and reads the `mass` field:

```python
mass = meteorite.get("mass")
```

Missing or empty values are skipped:

```python
if mass in (None, ""):
    continue
```

Mass values are stored as strings in the dataset, so valid values are converted
to numbers before comparison:

```python
try:
    numeric_mass = float(mass)
except (TypeError, ValueError):
    continue
```

This ensures that masses are compared numerically rather than as strings.

The largest valid mass found is:

```text
Sikhote-Alin — 23,000,000 g
```

### Most frequent year

The `year` field is parsed using `datetime.fromisoformat()`:

```python
parsed_year = datetime.fromisoformat(year).year
```

A `collections.Counter` is used to count how many times each year appears:

```python
years[parsed_year] += 1
```

The most frequent year is retrieved using:

```python
years.most_common(1)[0]
```

Result:

```text
1933 — 16 entries
```

## Error Handling

The script handles:

- HTTP and network errors
- HTTP error status codes
- malformed or invalid JSON
- unexpected JSON structures
- missing or invalid mass values
- missing or invalid year values

Errors are written to `stderr`, and the application returns a non-zero exit
code on failure.

## Running Locally

Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the solution:

```bash
python solution.py
```

Expected output:

```text
Number of entries: 1000
Most massive meteorite: Sikhote-Alin (23,000,000 g)
Most frequent year: 1933 (16 entries)
```

## Tests

Unit tests are implemented using `pytest`.

HTTP requests are mocked so that the tests are deterministic and do not depend
on external network availability.

The tests cover:

- successful JSON retrieval
- invalid JSON
- unexpected JSON structures
- network failures
- numeric mass comparison
- missing or invalid masses
- most frequent year calculation
- missing or invalid years

Run the tests with:

```bash
python -m pytest -v
```

## Docker

Docker was added to provide a consistent and reproducible runtime environment
for the solution.

The image contains the required Python runtime and installs the dependencies
defined in `requirements.txt`. This reduces problems caused by differences in
locally installed Python versions, packages, or host configuration.

Build the image:

```bash
docker build -t meteorites-homework .
```

Run the solution:

```bash
docker run --rm meteorites-homework
```

Run the tests inside the container:

```bash
docker run --rm meteorites-homework python -m pytest -v
```

The application runs as a non-root user inside the container and requires
outbound network access to retrieve the dataset.

## Design Considerations

The provided dataset contains only 1,000 records, so loading it into memory is
reasonable and keeps the implementation simple.

For a significantly larger JSON dataset, I would consider streaming the HTTP
response and processing records incrementally to keep memory usage bounded.

Retries with exponential backoff were intentionally not implemented because
this is a one-shot analysis script.

For an automated or scheduled production workload, bounded retries would be
appropriate for temporary network failures, rate limiting, or retryable server
errors.