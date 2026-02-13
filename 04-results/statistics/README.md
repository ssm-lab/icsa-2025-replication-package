## Statistics

These results are generated from `02-data/03-final-RA.xlsx` (sheet: `final-RA-to-framework-summary`)
by using `03-analysis/statistics_generator.py` script.


Each cell in the sheet `final-RA-to-framework-summary` that represents a mapping relation is classified into one of the following categories:
- `explicit` - Explicitly implemented component in the specific framework (i.e., standalone component).
- `implicit` - Implicitly implemented component in the specific framework (i.e., functionality is present but merged into another component).
- `external` - Implemented component via an external third-party dependency.
- `not implemented` - Component not implemented in the specific framework.


Reported values in `stats.txt`:
- Counts: number of occurrences of each category.
- Percentages:
  - explicit v.s. total: proportion of all that are explicitly implemented.
  - explicit v.s. implemented: among implemented components, how many are explicit.
  - implicit v.s. implemented: among implemented components, how many are implicit.
  - external v.s. implemented: among implemented components, how many rely on external libraries.
