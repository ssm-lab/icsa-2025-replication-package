from pathlib import Path
import re

import pandas as pd
import matplotlib.pyplot as plt


# -------------------------
# Paths
# -------------------------
ROOT = Path(__file__).resolve().parent.parent
XLSX_PATH = ROOT / "02-data" / "03-final-RA.xlsx"
SHEET = "final-RA-to-framework-summary"
OUT_PDF_DIR = ROOT / "04-results" / "tables" / "pdf"
OUT_TEX_DIR = ROOT / "04-results" / "tables" / "latex"
OUT_EXT = "pdf"
KEEP_CODES = {"explicit", "implicit", "external"}

# -------------------------
# Table configs
# -------------------------
TABLES = {
    "Experiment Orchestrator": {
        "tex": "experiment-orchestrator.tex",
        "caption": "Experiment Orchestrator Components",
        "label": "tab:ra-experiment-orchestrator",
        "colspec": r"@{}p{2.6cm}p{5.9cm}@{}",
        "vspace_cap": "-0.75em",
        "vspace_end": "-1em",
        "left_header": "Component",
        "right_header": "Frameworks",
    },
    "Framework Orchestrator": {
        "tex": "framework-orchestrator.tex",
        "caption": "Framework Orchestrator Components",
        "label": "tab:ra-framework-orchestrator",
        "colspec": r"@{}p{2.6cm}p{5.9cm}@{}",
        "vspace_cap": "-0.5em",
        "vspace_end": "-0.75em",
        "left_header": "Component",
        "right_header": "Frameworks",
    },
    "Agent": {
        "tex": "agent.tex",
        "caption": "Agent Components",
        "label": "tab:ra-agent",
        "colspec": r"@{}p{1.8cm}p{6.7cm}@{}",
        "vspace_cap": "-0.5em",
        "vspace_end": "-0.75em",
        "left_header": "Component",
        "right_header": "Frameworks",
    },
    "Environment": {
        "tex": "environment.tex",
        "caption": "Environment Components",
        "label": "tab:ra-environment",
        "colspec": r"@{}p{2.1cm}p{6.4cm}@{}",
        "vspace_cap": "-0.5em",
        "vspace_end": "-0.75em",
        "left_header": "Component",
        "right_header": "Frameworks",
    },
    "Data Persistence": {
        "tex": "data-persistence.tex",
        "caption": "Data Persistence Components",
        "label": "tab:ra-data-persistence",
        "colspec": r"@{}p{2cm}p{6.5cm}@{}",
        "vspace_cap": "-0.5em",
        "vspace_end": "-0.75em",
        "left_header": "Component",
        "right_header": "Frameworks",
    },
    "Monitoring & Visualization": {
        "tex": "monitoring-and-visualization.tex",
        "caption": r"Monitoring \& Visualization Components",
        "label": "tab:ra-monitoring-and-visualization",
        "colspec": r"@{}p{0.8cm}p{7.7cm}@{}",
        "vspace_cap": "0em",
        "vspace_end": "-0.75em",
        "left_header": "Comp.",
        "right_header": "Frameworks",
    },
}


def clean(x) -> str:
    if pd.isna(x):
        return ""
    return str(x).strip()


def rename(s: str) -> str:
    s = s.lower()
    s = s.replace("&", "and")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "table"


def fid_number(fid: str) -> int:
    return int(clean(fid)[1:])


def load_sheet():
    df = pd.read_excel(XLSX_PATH, sheet_name=SHEET, header=None, engine="openpyxl")
    f_ids = [clean(x) for x in df.iloc[0, 2:].tolist()]
    cite_keys = [clean(x) for x in df.iloc[1, 2:].tolist()]
    data = df.iloc[2:, :].copy()
    return data, f_ids, cite_keys


def collect_rows_for_group(data, f_ids, cite_keys, group_name: str):
    rows = []

    for _, r in data.iterrows():
        if clean(r[0]) != group_name:
            continue
        comp = clean(r[1])
        if comp == "":
            continue

        selected_fids = []
        selected_cites = []

        for j, (fid, ckey) in enumerate(zip(f_ids, cite_keys)):
            code = clean(r[2 + j]).lower()
            if code in KEEP_CODES:
                selected_fids.append(fid)
                selected_cites.append(ckey)

        pairs = list(zip(selected_fids, selected_cites))
        pairs.sort(key=lambda t: (fid_number(t[0]), t[0]))
        rows.append((comp, pairs))

    rows.sort(key=lambda t: t[0].lower())
    return rows


# -------------------------
# Latex output
# -------------------------
def latex_cites(pairs):
    return " ".join([rf"\cite{{{ckey}}}" for _, ckey in pairs if ckey])

def write_tex(spec, rows, out_path: Path):
    lines = []
    lines.append(r"\begin{table}[t]")
    lines.append(r"\centering")
    lines.append(rf"\caption{{{spec['caption']}}}")
    if spec["vspace_cap"] != "0em":
        lines.append(rf"\vspace{{{spec['vspace_cap']}}}")
    lines.append(rf"\label{{{spec['label']}}}")
    lines.append(r"\renewcommand{\arraystretch}{0.9}")
    lines.append(r"{\scriptsize")
    lines.append(rf"\begin{{tabular}}{{{spec['colspec']}}}")
    lines.append(r"\toprule")
    lines.append(
        rf"\multicolumn{{1}}{{c}}{{\textbf{{{spec['left_header']}}}}} & "
        rf"\multicolumn{{1}}{{c}}{{\textbf{{{spec['right_header']}}}}} \\ \midrule"
    )

    for comp, pairs in rows:
        lines.append(rf"{comp} & {latex_cites(pairs)}\\")
        lines.append("")

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}}")
    if spec["vspace_end"] != "0em":
        lines.append(rf"\vspace{{{spec['vspace_end']}}}")
    lines.append(r"\end{table}")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")


# -------------------------
# PDF figure output
# -------------------------
def write_pdf(spec, rows, out_path: Path):
    PER_LINE = 5
    table_data = []
    max_lines = 1

    for comp, pairs in rows:
        fids = [fid for fid, _ in pairs]
        fids.sort(key=lambda x: (fid_number(x), x))

        tokens = [f"[{fid}]" for fid in fids]
        lines = [" ".join(tokens[i:i + PER_LINE]) for i in range(0, len(tokens), PER_LINE)]
        text = "\n".join(lines)

        table_data.append([comp, text])
        max_lines = max(max_lines, len(lines) if lines else 1)

    out_path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(
        figsize=(5, 2 + 0.6 * len(rows) + 0.4 * (max_lines - 1)),
        dpi=250
    )
    ax.axis("off")
    ax.set_title(spec["caption"], fontsize=11, pad=12)

    t = ax.table(
        cellText=table_data,
        colLabels=[spec["left_header"], spec["right_header"]],
        cellLoc="left",
        loc="upper center",
    )
    t.auto_set_font_size(False)
    t.set_fontsize(10)
    t.scale(1, 1.4 + 0.6 * (max_lines - 1))

    for (r, c), cell in t.get_celld().items():
        if r == 0:
            cell.set_text_props(weight="bold")

    plt.tight_layout()
    fig.savefig(out_path, bbox_inches="tight")
    plt.close(fig)


def main():
    data, f_ids, cite_keys = load_sheet()

    for group_name, spec in TABLES.items():
        rows = collect_rows_for_group(data, f_ids, cite_keys, group_name)
        if not rows:
            continue

        # PDF
        pdf_path = OUT_PDF_DIR / f"{rename(group_name)}.{OUT_EXT}"
        write_pdf(spec, rows, pdf_path)

        # Latex
        tex_path = OUT_TEX_DIR / spec["tex"]
        write_tex(spec, rows, tex_path)

    print("Done.")
    print("PDF/PNG saved to:", OUT_PDF_DIR)
    print("LaTeX saved to:", OUT_TEX_DIR)


if __name__ == "__main__":
    main()

