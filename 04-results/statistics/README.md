## Statistics

Report of component types in the analyzed frameworks.

Reported values in `stats.txt`:
- `Counts` - Number of occurrences of each category. (See [Categories](#Categories) below.)
- `Percentages`
  - `explicit vs total` - The ratio of explicitly implemented components among all possible components (implemented or not implemented).
  - `explicit vs implemented` - The ratio of explicitly implemented components among all implemented components.
  - `implicit vs implemented` - The ratio of implicitly implemented components among all implemented components
  - `external vs implemented` - The ratio of components implemented via external (third-party) libraries among all implemented components.

These results are generated from `02-data/03-final-RA.xlsx` (sheet: `final-RA-to-framework-summary`)
by using `03-analysis/statistics_generator.py` script.

#### Categories
Each cell in the sheet `final-RA-to-framework-summary` that represents a mapping relation is classified into one of the following categories:
- `explicit` - Explicitly implemented component in the specific framework (i.e., standalone component).
- `implicit` - Implicitly implemented component in the specific framework (e.g., functionality is present but merged into another component).
- `external` - Implemented component via an external third-party dependency.
- `not implemented` - Component not implemented in the specific framework.
