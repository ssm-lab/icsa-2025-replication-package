from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

# -------------------------
# Paths
# -------------------------
ROOT = Path(__file__).resolve().parent.parent
XLSX_PATH = ROOT / "02-data" / "03-final-RA.xlsx"
SHEET = "final-RA-to-framework-summary"
OUT_DIR = ROOT / "04-results"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -------------------------
# Constants
# -------------------------
ROW_FID = 0
ROW_NAME = 1
ROW_CITE = 2
ROW_DATA_START = 3
CATEGORIES = {"external", "implicit", "explicit"}
FRAMEWORK_SYSTEMS = {
    "Unity ML-Agents",
    "Stable Baselines3",
    "RL Baselines3 Zoo",
    "RLlib",
    "Acme",
    "MARLlib",
    "BenchMARL",
    "Mava",
    "Dopamine",
    "Tianshou",
}
ENVIRONMENT_SYSTEMS = {
    "Gymnasium",
    "PettingZoo",
    "Isaac Gym",
    "Isaac Lab",
    "dm_control",
    "DeepMind Lab",
    "Arcade Learning Environment",
    "Jumanji",
}

COMPONENT_RENAME = {
    "Experiment Orchestrator": "Experiment\nOrchestrator",
    "Experiment Manager": "Experiment\nManager",
    "Hyperparameter Tuner": "Hyperparam.\nTuner",
    "Benchmark Manager": "Benchmark\nManager",
    "Framework Orchestrator": "Framework\nOrchestrator",
    "Lifecycle Manager": "Lifecycle Mgr.",
    "Configuration Manager": "Config. Mgr.",
    "Multi-Agent Coordinator": "Multi-Agent\nCoord.",
    "Distributed Execution Coordinator": "Distributed\nExec. Coord.",
    "Agent": "Agent",
    "Function Approximator": "Func. Approx.",
    "Buffer": "Buffer",
    "Learner":  "Learner",
    "Environment": "Environment",
    "Environment Core": "Environment\nCore",
    "Simulator": "Simulator",
    "Simulator Adapter": "Simulator\nAdapter",
    "Data Persistence": "Data\nPersistence",
    "Checkpoint Manager": "Checkpoint\nManager",
    "Environment Parameter Manager": "Env. Param.\nManager",
    "Monitoring & Visualization": "Monitoring &\nVisualization",
    "Renderer": "Renderer",
    "Recorder": "Recorder",
    "Logger": "Logger",
    "Reporter": "Reporter",
}

KEEP_COMPONENTS = {
    "Experiment Orchestrator",
    "Experiment Manager",
    "Hyperparameter Tuner",
    "Benchmark Manager",
    "Framework Orchestrator",
    "Lifecycle Manager",
    "Configuration Manager",
    "Multi-Agent Coordinator",
    "Distributed Execution Coordinator",
    "Agent",
    "Function Approximator",
    "Buffer",
    "Learner",
    "Environment",
    "Environment Core",
    "Simulator",
    "Simulator Adapter",
}

KEEP_COMPONENTS_UTILITIES = {
    "Data Persistence",
    "Checkpoint Manager",
    "Environment Parameter Manager",
    "Monitoring & Visualization",
    "Renderer",
    "Recorder",
    "Logger",
    "Reporter",
}

MANUAL_ORDER = [
    "Agent",
    "Buffer",
    "Function Approximator",
    "Learner",
    "Framework Orchestrator",
    "Experiment Manager",
    "Lifecycle Manager",
    "Multi-Agent Coordinator",
    "Configuration Manager",
    "Distributed Execution Coordinator",
    "Hyperparameter Tuner",
    "Experiment Orchestrator",
    "Benchmark Manager",
    "Simulator Adapter",
    "Simulator",
    "Environment",
    "Environment Core",
]

MANUAL_ORDER_UTILITIES = [
    "Environment Parameter Manager",
    "Checkpoint Manager",
    "Data Persistence",
    "Monitoring & Visualization",
    "Logger",
    "Recorder",
    "Renderer",
    "Reporter",
]


def clean(x) -> str:
    if pd.isna(x):
        return ""
    return str(x).strip()

def build_heatmap_df(keep_components,manual_order=None):
    df_raw = pd.read_excel(XLSX_PATH, sheet_name=SHEET, header=None, engine="openpyxl")

    names = {}
    for col_idx, val in enumerate(df_raw.iloc[ROW_NAME, 2:], start=2):
        if pd.isna(val):
            name = ""
        else:
            name = " ".join(str(val).split())
        names[col_idx] = name

    data = df_raw.iloc[ROW_DATA_START:, :].copy().reset_index(drop=True)

    records = []
    for _, row in data.iterrows():
        if pd.isna(row.iloc[1]):
            name = ""
        else:
            name = " ".join(str(row.iloc[1]).split())

        if not name or name == "nan":
            continue

        framework_counts  = {k: 0 for k in CATEGORIES}
        environment_counts = {k: 0 for k in CATEGORIES}

        for col_idx, val in enumerate(row.iloc[2:], start=2):
            code = clean(val)
            sys_name = names.get(col_idx, "")
            if code in framework_counts:
                if sys_name in FRAMEWORK_SYSTEMS:
                    framework_counts[code] += 1
                elif sys_name in ENVIRONMENT_SYSTEMS:
                    environment_counts[code] += 1

        records.append({
            "component":    name,
            "framework_implicit": framework_counts["implicit"],
            "framework_external":  framework_counts["external"],
            "framework_explicit":  framework_counts["explicit"],
            "environment_implicit": environment_counts["implicit"],
            "environment_external": environment_counts["external"],
            "environment_explicit": environment_counts["explicit"],
        })

    df = pd.DataFrame(records).set_index("component")
    df = df[df.index.isin(keep_components)]

    if manual_order is not None:
        df = df.reindex([c for c in manual_order if c in df.index])
    return df


def plot_heatmap(df):
    df = df.rename(index=COMPONENT_RENAME)
    fig, ax = plt.subplots(figsize=(7, 8))

    sns.heatmap(df, ax=ax, fmt="d", cmap="Blues", cbar=False, vmin=0)
    for r in range(df.shape[0]):
        for c in range(df.shape[1]):
            val = int(df.iloc[r, c])
            if val != 0:
                color = "white" if val >= 5 else "black"
                ax.text(c + 0.5, r + 0.5, str(val),
                        ha="center", va="center", fontsize=11, color=color)

    ax.axvline(x=3, color="white", linewidth=2.5)
    ax.set_xticklabels(
        ["Implicit", "External", "Explicit", "Implicit", "External", "Explicit"],
        rotation=0, fontsize=11
    )
    ax.text(0.25, 1.01, "Labeled as Framework", ha="center", va="bottom",
            fontsize=11, fontweight="bold", transform=ax.transAxes)
    ax.text(0.75, 1.01, "Labeled as Environment", ha="center", va="bottom",
            fontsize=11, fontweight="bold", transform=ax.transAxes)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, fontsize=11)
    ax.set_ylabel("")

    plt.tight_layout()
    return fig


def main():
    print("Building heatmap data…")
    df_core = build_heatmap_df(KEEP_COMPONENTS, MANUAL_ORDER)
    csv_path = OUT_DIR / "statistics" / "heatmap_data.csv"
    df_core.to_csv(csv_path)
    print(f"\nSaved CSV to {csv_path}")
    print("Plotting heatmap…")
    fig = plot_heatmap(df_core)
    fig.savefig(OUT_DIR / "plots" / "heatmap.png", dpi=250, bbox_inches="tight")
    fig.savefig(OUT_DIR / "plots" / "heatmap.pdf", bbox_inches="tight")
    plt.close(fig)
    print("Saved heatmap.")

    print("Building heatmap data for utilities…")
    df_util = build_heatmap_df(KEEP_COMPONENTS_UTILITIES, MANUAL_ORDER_UTILITIES)
    csv_path_util = OUT_DIR / "statistics" / "heatmap_data_util.csv"
    df_util.to_csv(csv_path_util)
    print(f"\nSaved CSV to {csv_path}")
    print("Plotting heatmap for utilities…")
    fig = plot_heatmap(df_util)
    fig.savefig(OUT_DIR / "plots" / "heatmap_util.png", dpi=250, bbox_inches="tight")
    fig.savefig(OUT_DIR / "plots" / "heatmap_util.pdf", bbox_inches="tight")
    plt.close(fig)
    print("Saved heatmap.")


if __name__ == "__main__":
    main()