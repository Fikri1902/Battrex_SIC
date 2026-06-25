"""Render grafik gelombang EoL (committed vs skenario ESDM) untuk laporan LaTeX."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent
dec = json.loads((BASE / "data" / "battrek_decrement_output.json").read_text(encoding="utf-8"))
auc = {int(k): v for k, v in dec["skenario_A_committed"]["unit_per_tahun"].items()}
auf = {int(k): v for k, v in dec["skenario_B_esdm"]["unit_per_tahun"].items()}
yrs = sorted(auf)

NAVY = "#0f2c59"; RED = "#dc2626"; ORANGE = "#f59e0b"
fig, ax = plt.subplots(figsize=(9, 5))
ax.fill_between(yrs, [auc[y] for y in yrs], color=ORANGE, alpha=0.25)
ax.plot(yrs, [auf[y] for y in yrs], "-o", color=RED, lw=2.5, ms=4, label="+ skenario pertumbuhan (anchor ESDM)")
ax.plot(yrs, [auc[y] for y in yrs], "-o", color=ORANGE, lw=2.5, ms=4, label="committed (mobil yang sudah terjual)")
ax.axvline(2032, color="#9ca3af", ls="--", lw=1)
ax.annotate("puncak committed 2032\n~29.500 unit", xy=(2032, auc[2032]),
            xytext=(2033.2, auc[2032] + 8000), fontsize=9, color=NAVY,
            arrowprops=dict(arrowstyle="->", color="#9ca3af"))
ax.set_title("Proyeksi Gelombang Baterai Mobil Listrik Pensiun per Tahun (Indonesia)",
             fontsize=12.5, fontweight="bold", color=NAVY)
ax.set_xlabel("Tahun"); ax.set_ylabel("Baterai pensiun (unit)")
ax.legend(fontsize=9, loc="upper left"); ax.grid(alpha=0.25)
ax.spines[["top", "right"]].set_visible(False)
ax.ticklabel_format(style="plain", axis="y")
out = BASE / "figures" / "grafik_gelombang_eol.png"
fig.savefig(out, dpi=150, bbox_inches="tight")
print("Tersimpan:", out)
