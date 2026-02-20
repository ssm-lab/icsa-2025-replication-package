from pathlib import Path
import pandas as pd

# -------------------------
# Paths
# -------------------------
ROOT = Path(__file__).resolve().parent.parent  # root/
XLSX_PATH = ROOT / "02-data" / "03-final-RA.xlsx"
SHEET = "final-RA-to-framework-summary"
OUT_DIR = ROOT / "04-results" / "statistics"
OUT_PATH = OUT_DIR / "stats.txt"
CODES = {"explicit", "implicit", "external", "not implemented"}

# -------------------------
# Constants
# -------------------------
ROW_DATA_START = 3
CATEGORIES = ["explicit", "implicit", "external"]

def clean(x) -> str:
    if pd.isna(x):
        return ""
    return str(x).strip()

def safe_div(a, b):
    if b != 0:
        return a / b
    else:
        return 0.0

def safe_pct(numerator, denominator) -> float:
    if denominator == 0:
        return 0.0
    return (numerator / denominator) * 100

def load_data():
    df_raw = pd.read_excel(XLSX_PATH, sheet_name=SHEET, header=None, engine="openpyxl")
    data   = df_raw.iloc[ROW_DATA_START:, :].copy().reset_index(drop=True)

    records = []
    for _, row in data.iterrows():
        if pd.isna(row.iloc[0]):
            group = ""
        else:
            group = " ".join(str(row.iloc[0]).split())
        if pd.isna(row.iloc[1]):
            name = ""
        else:
            name = " ".join(str(row.iloc[1]).split())
        if not name or name == "nan":
            continue
        counts = {k: 0 for k in CATEGORIES}
        for val in row.iloc[2:]:
            code = clean(val).lower()
            if code in counts:
                counts[code] += 1
        records.append({"component": name, "group": group, **counts})

    return pd.DataFrame(records).set_index("component")



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


def stats_category_report(df, category, threshold=0.5):
    n_total = len(df)
    lines   = [
        "=" * 74,
        f"Category: {category}",
        "=" * 74,
        f"  {'Component':45} {'Count':>6} {'% of implemented':>18}",
        "  " + "-" * 72,
    ]
    rows = []
    for comp, row in df.iterrows():
        implemented = row["explicit"] + row["implicit"] + row["external"]
        if implemented > 0:
            pct = safe_pct(row[category], implemented)
        else:
            pct = 0.0
        rows.append((comp, int(row[category]), implemented, pct, row["group"]))

    rows.sort(key=lambda x: x[3], reverse=True)

    exceeded = 0
    for comp, count, implemented, pct, group in rows:
        if pct > threshold * 100:
            exceeded += 1
        lines.append(
            f"  {comp:45} {count:>6} / {int(implemented):<5}  {pct:5.1f}%"
        )
    lines.append("")
    lines.append(f"  Components exceeding {int(threshold * 100)}%: {exceeded} / {n_total}")
    lines.append(f"  Proportion: {exceeded}/{n_total} = {safe_pct(exceeded, n_total):.1f}%")

    return lines


def main():
    print("Loading data …")
    df = load_data()
    calculate_stats()
    print(f"Saved basic statistics to {OUT_PATH}")
    for cat in CATEGORIES:
        cat_lines = stats_category_report(df, category=cat, threshold=0.5)
        cat_path  = OUT_DIR / f"stats_{cat}.txt"
        cat_path.write_text("\n".join(cat_lines) + "\n", encoding="utf-8")
        print(f"Saved each status's statistics to {cat_path}")

if __name__ == "__main__":
    main()
