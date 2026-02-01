# Meteorite Landings Analysis - Pull Request

## Summary

This PR adds a reproducible Python analysis that answers all three required questions using the provided dataset.

## Results (as of 2026-02-01)

- Total entries: **1,000**
- Most massive meteorite: **Sikhote-Alin** — **23,000,000 grams** (23,000.0 kg)
- Most frequent year: **1933** — **16** landings

Results were computed programmatically and saved to `analysis/results/analysis_report.txt`.

## How the results were computed

- Fetch the JSON dataset from the provided URL.
- Count all records for the total entry count.
- Parse valid mass values, then select the maximum by numeric mass.
- Parse valid year values (including ISO 8601 strings), count frequencies, and pick the most frequent year.
- The script skips invalid or missing values rather than failing.

## How to run

```bash
cd analysis
python3 meteorite_analysis.py
```

## Files added/updated

- `analysis/meteorite_analysis.py` — analysis script
- `analysis/results/analysis_report.txt` — generated report
- `docs/ANALYSIS.md` — methodology description
- `README.md` — quick start + overview
