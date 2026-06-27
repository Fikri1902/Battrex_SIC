"""
BATTREX — Panel 1 'Fakta Global'.
Donut: pangsa mobil listrik dunia (World EV sales share) 2025, dibaca langsung dari
EV Data Explorer 2026 (IEA) agar akurat. + callout: Eropa sudah punya regulasi baterai.
Output: ../06_ASET_VISUAL/viz_fakta_global.png
"""
from pathlib import Path
import openpyxl
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parent.parent
xlsx = BASE / "02_DATA" / "excel" / "EV Data Explorer 2026.xlsx"
wb = openpyxl.load_workbook(xlsx, read_only=True, data_only=True)
ws = wb["GEVO_EV_2026"]; hdr = None; world = {}
for r in ws.iter_rows(values_only=True):
    if hdr is None: hdr = list(r); continue
    d = dict(zip(hdr, r))
    if (str(d.get("region_country")).strip() == "World" and str(d.get("parameter")) == "EV sales share"
            and str(d.get("mode")) == "Cars" and str(d.get("powertrain")) == "EV"):
        try: world[int(d["year"])] = float(d["value"])
        except: pass
share = round(world.get(2025, 25))
print("World EV sales share 2025 =", world.get(2025), "-> dipakai:", share, "%")

NAVY="#0f2c59"; TEAL="#0ea5e9"; GREY="#e2e8f0"; GREEN="#16a34a"
fig, (axd, axt) = plt.subplots(1, 2, figsize=(11, 5), gridspec_kw={"width_ratios":[1, 1.15]})

# Donut "1 dari 4"
axd.pie([share, 100-share], colors=[TEAL, GREY], startangle=90, counterclock=False,
        wedgeprops=dict(width=0.42, edgecolor="white"))
axd.text(0, 0.12, f"{share}%", ha="center", va="center", fontsize=40, fontweight="bold", color=NAVY)
axd.text(0, -0.22, "mobil baru dunia\nkini listrik (2025)", ha="center", va="center", fontsize=11, color="#475569")
axd.set_title("~ 1 dari 4 mobil baru di dunia", fontsize=13, fontweight="bold", color=NAVY)

# Callout Eropa
axt.axis("off")
axt.text(0.0, 0.93, "DUNIA SUDAH BERGERAK,", fontsize=15, fontweight="bold", color=NAVY)
axt.text(0.0, 0.82, "DAN YANG TERDEPAN SUDAH SIAP.", fontsize=15, fontweight="bold", color=NAVY)
axt.text(0.0, 0.62, "Transisi ke kendaraan listrik menjadi tren global.\n"
                    "Kawasan maju seperti Uni Eropa bahkan telah\n"
                    "lebih dulu mewajibkan pelacakan & pengelolaan\n"
                    "siklus hidup baterai (paspor baterai).",
         fontsize=11.5, color="#334155", va="top", linespacing=1.4)
axt.add_patch(plt.Rectangle((0.0, 0.18), 0.96, 0.18, color=GREEN, alpha=0.12,
              transform=axt.transAxes))
axt.text(0.03, 0.27, "Uni Eropa: Regulation (EU) 2023/1542 - paspor baterai wajib.",
         fontsize=11, fontweight="bold", color=GREEN, va="center")
axt.text(0.0, 0.04, "Sumber: IEA Global EV Outlook 2026; Regulation (EU) 2023/1542.",
         fontsize=8, color="#94a3b8")

out = BASE / "06_ASET_VISUAL" / "viz_fakta_global.png"
fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
print("OK", out.name)
