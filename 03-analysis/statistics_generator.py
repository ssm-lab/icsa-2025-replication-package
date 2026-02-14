from pathlib import Path
import pandas as pd

# -------------------------
# Paths
# -------------------------
ROOT = Path(__file__).resolve().parent.parent  # root/
XLSX_PATH = ROOT / "02-data" / "03-final-RA.xlsx"
SHEET = "final-RA-to-framework-summary"
OUT_PATH = ROOT / "04-results" / "statistics" / "stats.txt"
CODES = {"explicit", "implicit", "external", "not implemented"}

# -------------------------
# Constants
# -------------------------
ROW_DATA_START = 3


def clean(x) -> str:
    if pd.isna(x):
        return ""
    return str(x).strip()

def safe_div(a, b):
    if b != 0:
        return a / b
    else:
        return 0.0

def calculate_stats():
    df = pd.read_excel(XLSX_PATH, sheet_name=SHEET, header=None, engine="openpyxl")
    data = df.iloc[ROW_DATA_START:, :].copy()
    counts = {}
    for k in CODES:
        counts[k] = 0
    for _, r in data.iterrows():
        for v in r.iloc[2:]:
            code = clean(v).lower()
            if code in counts:
                counts[code] += 1

    total = sum(counts.values())
    implemented = counts["explicit"] + counts["implicit"] + counts["external"]

    stats = {
        "explicit vs total": safe_div(counts["explicit"], total),
        "explicit vs implemented": safe_div(counts["explicit"], implemented),
        "implicit vs implemented": safe_div(counts["implicit"], implemented),
        "external vs implemented": safe_div(counts["external"], implemented),
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    lines = []
    lines.append("=" * 40)
    lines.append("Statistics Summary")
    lines.append("=" * 40)
    lines.append("Counts")
    lines.append("-" * 40)
    lines.append(f"{'explicit':30} | {counts['explicit']}")
    lines.append(f"{'implicit':30} | {counts['implicit']}")
    lines.append(f"{'external':30} | {counts['external']}")
    # lines.append(f"  implemented:      {implemented}  (explicit+implicit+external)")
    lines.append(f"{'not implemented':30} | {counts['not implemented']}")
    lines.append(f"{'total':30} | {total}")
    lines.append("")
    lines.append("Percentages")
    lines.append("-" * 40)
    for k, v in stats.items():
        lines.append(f"{k:30} | {v * 100:.2f}%")

    OUT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Saved:", OUT_PATH)


if __name__ == "__main__":
    calculate_stats()
