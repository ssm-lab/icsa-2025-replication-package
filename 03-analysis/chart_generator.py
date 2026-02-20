from pathlib import Path
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# -------------------------
# Paths
# -------------------------
ROOT = Path(__file__).resolve().parent.parent
XLSX_PATH = ROOT / "02-data" / "03-final-RA.xlsx"
SHEET = "final-RA-to-framework-summary"
OUT_DIR = ROOT / "04-results" / "plots"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------
# Constants
# -------------------------
ROW_FID = 0
ROW_CITE = 2
ROW_DATA_START = 3
CATEGORIES = ["explicit", "implicit", "external"]
COLORS = {
    "explicit": "#A8CD89",
    "implicit": "#F4E0AF",
    "external": "#F9C0AB",
}
LABELS = {
    "explicit": "Explicit",
    "implicit": "Implicit",
    "external": "External",
}

def clean(x) -> str:
    if pd.isna(x):
        return ""
    return str(x).strip()

def sort_data(df):
    df["total"] = df[CATEGORIES].sum(axis=1)
    df = df.sort_values(
        by=["total", "explicit", "implicit", "external"],
        ascending=False
    )
    df = df.drop(columns="total")
    return df

def load_data():
    df = pd.read_excel(XLSX_PATH, sheet_name=SHEET, header=None, engine="openpyxl")
    data = df.iloc[ROW_DATA_START:, :].copy().reset_index(drop=True)

    component_names = data.iloc[:, 1].apply(lambda x: str(x).strip() if not pd.isna(x) else "")
    records = []
    for idx, row in data.iterrows():
        name = component_names.iloc[idx]
        if not name or name == "nan":
            continue
        counts = {k: 0 for k in CATEGORIES}
        for val in row.iloc[2:]:
            code = clean(val)
            if code in counts:
                counts[code] += 1
        counts["component"] = name
        records.append(counts)
    result_df = pd.DataFrame(records).set_index("component")
    result_df = sort_data(result_df)
    # print(result_df.head(10))
    return result_df


def _build_stacked_bars(ax, df, orientation="horizontal"):
    pos    = np.arange(len(df))
    offset = np.zeros(len(df))

    for cat in CATEGORIES:
        values = df[cat].values.astype(float)

        if orientation == "horizontal":
            bars = ax.barh(pos, values, left=offset,
                           color=COLORS[cat], label=LABELS[cat],
                           edgecolor="white", linewidth=0.5, height=0.5)
        else:
            bars = ax.bar(pos, values, bottom=offset,
                          color=COLORS[cat], label=LABELS[cat],
                          edgecolor="white", linewidth=0.5, width=0.5)

        for bar, val, o in zip(bars, values, offset):
            if val > 0:
                if orientation == "horizontal":
                    cx, cy = o + val / 2, bar.get_y() + bar.get_height() / 2
                else:
                    cx, cy = bar.get_x() + bar.get_width() / 2, o + val / 2
                ax.text(cx, cy, str(int(val)),
                        ha="center", va="center",
                        fontsize=7.5, color="black", fontweight="bold")
        offset += values

    for i, total in enumerate(offset):
        if orientation == "horizontal":
            ax.text(total + 0.1, i, str(int(total)),
                    ha="left", va="center",
                    fontsize=7.5, color="black", fontweight="bold")
        else:
            ax.text(i, total + 0.1, str(int(total)),
                    ha="center", va="bottom",
                    fontsize=7.5, color="black", fontweight="bold")


def _add_legend(ax):
    legend_patches = [
        mpatches.Patch(color=COLORS[cat], label=LABELS[cat])
        for cat in reversed(CATEGORIES)
    ]
    ax.legend(handles=legend_patches, fontsize=9,
              framealpha=0.9, edgecolor="lightgrey")


def plot_chart_horizontal(df):
    fig, ax = plt.subplots(figsize=(11, max(4, len(df) * 0.3 + 1)))
    _build_stacked_bars(ax, df, orientation="horizontal")
    ax.set_yticks(np.arange(len(df)))
    ax.set_yticklabels(df.index, fontsize=9)
    ax.invert_yaxis()
    ax.set_xlabel("Number of Frameworks", fontsize=10)
    ax.xaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
    ax.set_xlim(0, df[CATEGORIES].sum(axis=1).max() + 1)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    # ax.set_title("Implementation Status of Components across Analyzed RL Frameworks",
    #              fontsize=11, fontweight="bold", pad=12)
    _add_legend(ax)
    plt.tight_layout()
    return fig


def plot_chart_vertical(df):
    fig, ax = plt.subplots(figsize=(max(8, len(df) * 0.3 + 1), 5))
    _build_stacked_bars(ax, df, orientation="vertical")
    ax.set_xticks(np.arange(len(df)))
    ax.set_xticklabels(df.index, fontsize=7, rotation=45, ha="right")
    # ax.set_ylabel("Number of Frameworks", fontsize=10)
    # ax.yaxis.set_major_locator(matplotlib.ticker.MaxNLocator(integer=True))
    # ax.set_ylim(0, df[CATEGORIES].sum(axis=1).max() + 1)
    ax.set_xlim(-0.5, len(df) - 0.5)
    ax.yaxis.set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    # ax.set_title("Implementation Status of Components across Analyzed RL Frameworks",
    #              fontsize=11, fontweight="bold", pad=12)
    _add_legend(ax)
    plt.tight_layout()
    return fig


def main():
    print("Loading data …")
    df = load_data()
    print(f" Found {len(df)} components")
    print("Plotting …")
    fig_h = plot_chart_horizontal(df)
    fig_h.savefig(OUT_DIR / "bar_chart_horizontal.png", dpi=250, bbox_inches="tight")
    fig_h.savefig(OUT_DIR / "bar_chart_horizontal.pdf", bbox_inches="tight")
    plt.close(fig_h)
    print("Saved horizontal.")
    fig_v = plot_chart_vertical(df)
    fig_v.savefig(OUT_DIR / "bar_chart_vertical.png", dpi=250, bbox_inches="tight")
    fig_v.savefig(OUT_DIR / "bar_chart_vertical.pdf", bbox_inches="tight")
    plt.close(fig_v)
    print("Saved vertical.")


if __name__ == "__main__":
    main()


