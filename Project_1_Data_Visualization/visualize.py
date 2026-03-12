"""
Gaza Humanitarian Crisis — Data Visualization
==============================================
Author : Hala Anqawi
Tools  : Python · pandas · matplotlib · seaborn
Data   : Based on OCHA / WHO / UNRWA public reports (2023–2024)

This script produces a four-panel analytical figure covering:
  1. Cumulative casualties over time
  2. Infrastructure destruction breakdown
  3. Population displacement
  4. Humanitarian aid gap (trucks needed vs. entered)
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch
import numpy as np
import pandas as pd
import warnings, sys, os

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))
from dataset import (
    load_casualty_data, load_infrastructure_data,
    load_displacement_data, load_aid_data
)

# ── Palette ─────────────────────────────────────────────────────────────────
BG        = "#f5f0e8"
INK       = "#1a1714"
RUST      = "#c4451c"
RUST_DARK = "#9b3315"
RUST_PALE = "#f0c4b4"
SAND      = "#e8dfc8"
MUTED     = "#8a7f72"
LINE      = "#d4c9b8"

def style_axis(ax, title="", xlabel="", ylabel="", grid_axis="y"):
    ax.set_facecolor(BG)
    ax.spines[["top","right"]].set_visible(False)
    ax.spines[["left","bottom"]].set_color(LINE)
    ax.tick_params(colors=MUTED, labelsize=7.5)
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_fontfamily("monospace")
        label.set_color(MUTED)
    if title:
        ax.set_title(title, fontsize=9.5, color=INK, fontweight="bold",
                     fontfamily="serif", loc="left", pad=10)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=7.5, color=MUTED, fontfamily="monospace")
    if ylabel:
        ax.set_ylabel(ylabel, fontsize=7.5, color=MUTED, fontfamily="monospace")
    if grid_axis:
        ax.grid(axis=grid_axis, color=LINE, linewidth=0.6, linestyle="--", alpha=0.7)
        ax.set_axisbelow(True)

# ── Figure setup ─────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(16, 12), facecolor=BG)
fig.patch.set_facecolor(BG)

gs = gridspec.GridSpec(
    2, 2, figure=fig,
    hspace=0.42, wspace=0.38,
    left=0.07, right=0.96, top=0.84, bottom=0.07
)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[1, 0])
ax4 = fig.add_subplot(gs[1, 1])

# ── Header ───────────────────────────────────────────────────────────────────
fig.text(0.07, 0.93, "Gaza — Humanitarian Crisis Data Analysis",
         fontsize=22, color=INK, fontfamily="serif", fontweight="bold", va="bottom")
fig.text(0.07, 0.895,
         "Visualizing casualty trends, infrastructure loss, displacement & aid access  ·  Oct 2023 – Oct 2024",
         fontsize=9.5, color=MUTED, fontfamily="monospace")

# Thin rule under header
fig.add_artist(plt.Line2D([0.07, 0.96], [0.885, 0.885],
               transform=fig.transFigure, color=LINE, linewidth=0.8))

# Source footnote
fig.text(0.07, 0.012,
         "Data sources: OCHA Situation Reports · WHO Health Cluster · UNRWA Emergency Updates · Ministry of Health Gaza (2023–2024) · Figures are approximations.",
         fontsize=7, color=MUTED, fontfamily="monospace", style="italic")

# ── Panel 1 — Cumulative Casualties ──────────────────────────────────────────
df_c = load_casualty_data()
x = np.arange(len(df_c))

ax1.fill_between(x, df_c["injured"], alpha=0.15, color=RUST, zorder=1)
ax1.fill_between(x, df_c["killed"],  alpha=0.25, color=RUST, zorder=2)
ax1.plot(x, df_c["injured"], color=RUST_PALE, linewidth=1.8, zorder=3, label="Injured")
ax1.plot(x, df_c["killed"],  color=RUST,      linewidth=2.2, zorder=4, label="Killed")
ax1.plot(x, df_c["children_killed"], color=INK, linewidth=1.4,
         linestyle="--", zorder=5, label="Children killed")
ax1.plot(x, df_c["women_killed"], color=MUTED, linewidth=1.2,
         linestyle=":", zorder=5, label="Women killed")

ax1.set_xticks(x)
ax1.set_xticklabels(df_c["month"], rotation=45, ha="right", fontsize=7)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{int(v/1000)}k"))

# Annotate final value
ax1.annotate(f"{df_c['killed'].iloc[-1]//1000}k+",
             xy=(x[-1], df_c["killed"].iloc[-1]),
             xytext=(-28, 8), textcoords="offset points",
             fontsize=8, color=RUST, fontfamily="monospace",
             arrowprops=dict(arrowstyle="-", color=RUST, lw=0.8))

legend = ax1.legend(fontsize=7, frameon=True, loc="upper left",
                    facecolor=BG, edgecolor=LINE, labelcolor=MUTED)
style_axis(ax1, "Cumulative Casualties Over Time", ylabel="People")

# ── Panel 2 — Infrastructure Damage ──────────────────────────────────────────
df_i = load_infrastructure_data()
y_pos = np.arange(len(df_i))

bars = ax2.barh(y_pos, df_i["pct_destroyed"], color=RUST, alpha=0.85, height=0.55, zorder=3)
ax2.barh(y_pos, [100]*len(df_i), color=SAND, height=0.55, zorder=2)

for bar, row in zip(bars, df_i.itertuples()):
    ax2.text(bar.get_width() + 1.5, bar.get_y() + bar.get_height()/2,
             f"{row.pct_destroyed}%  ({row.count:,})",
             va="center", fontsize=7.2, color=INK, fontfamily="monospace")

ax2.set_yticks(y_pos)
ax2.set_yticklabels(df_i["category"], fontsize=7.5, fontfamily="monospace")
ax2.set_xlim(0, 130)
ax2.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{int(v)}%"))
style_axis(ax2, "Infrastructure — % Destroyed or Damaged", grid_axis="x")
ax2.spines["bottom"].set_visible(False)
ax2.tick_params(axis="x", bottom=False, labelbottom=False)

# ── Panel 3 — Displacement ────────────────────────────────────────────────────
df_d = load_displacement_data()
theta = np.linspace(0, 2*np.pi, 300)

# Proportional bubble chart
max_val = df_d["people"].max()
bubble_r = np.sqrt(df_d["people"] / max_val) * 0.38

cx = [0.18, 0.50, 0.78, 0.50]
cy = [0.50, 0.75, 0.50, 0.25]

ax3.set_xlim(0, 1); ax3.set_ylim(0, 1)
ax3.set_aspect("equal")
ax3.axis("off")
ax3.set_facecolor(BG)
ax3.set_title("Population Displacement", fontsize=9.5, color=INK,
              fontweight="bold", fontfamily="serif", loc="left", pad=10)

colors_fill = [SAND, RUST_PALE, RUST, "#e07b5a"]
for i, row in df_d.iterrows():
    circle = plt.Circle((cx[i], cy[i]), bubble_r[i],
                         color=colors_fill[i], alpha=0.7, zorder=3)
    ax3.add_patch(circle)
    ax3.text(cx[i], cy[i] + 0.01, f"{row['people']/1_000_000:.1f}M",
             ha="center", va="center", fontsize=9, fontweight="bold",
             color=INK, fontfamily="monospace", zorder=4)
    ax3.text(cx[i], cy[i] - bubble_r[i] - 0.06,
             row["phase"].replace("\n", " "),
             ha="center", va="top", fontsize=7, color=MUTED,
             fontfamily="monospace", zorder=4)

# ── Panel 4 — Aid Gap ────────────────────────────────────────────────────────
df_a = load_aid_data()
x = np.arange(len(df_a))
w = 0.38

ax4.bar(x - w/2, df_a["needed"],  w, color=SAND,  label="Trucks needed/day",  zorder=3)
ax4.bar(x + w/2, df_a["entered"], w, color=RUST,   label="Trucks entered/day", zorder=3)

for xi, needed, entered in zip(x, df_a["needed"], df_a["entered"]):
    pct = entered / needed * 100
    ax4.text(xi + w/2, entered + 4, f"{pct:.0f}%",
             ha="center", fontsize=6.5, color=RUST_DARK, fontfamily="monospace")

ax4.set_xticks(x)
ax4.set_xticklabels(df_a["month"], rotation=45, ha="right", fontsize=7)
legend = ax4.legend(fontsize=7, frameon=True, facecolor=BG, edgecolor=LINE, labelcolor=MUTED)
style_axis(ax4, "Humanitarian Aid Access Gap", ylabel="Trucks per day")

# ── Save ──────────────────────────────────────────────────────────────────────
out = "/mnt/user-data/outputs/gaza_data_visualization.png"
plt.savefig(out, dpi=180, bbox_inches="tight", facecolor=BG)
print(f"Saved → {out}")
plt.close()
