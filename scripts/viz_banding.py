"""
BATTREX — grafik perbandingan internasional pangsa penjualan mobil listrik (EV share).
Sumber: IEA Global EV Outlook 2026 (EV Data Explorer), parameter 'EV sales share', Cars, EV (BEV+PHEV), %.
Output: ../figures/viz_banding_asean_eu.png
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures"
NAVY="#0f2c59"; TEAL="#0ea5e9"; ORANGE="#f59e0b"; GREY="#cbd5e1"

# IEA EV sales share (Cars, %) — 2024 & 2025
data = [   # (label, 2024, 2025, kategori)
 ("Singapura", 34, 37, "asean"),
 ("Uni Eropa", 21, 27, "eu"),
 ("Vietnam", 19, 40, "asean"),
 ("Thailand", 13, 23, "asean"),
 ("Indonesia", 6.8, 15, "indo"),
 ("Malaysia", 3.1, 7, "asean"),
]
labels=[d[0] for d in data]; v24=[d[1] for d in data]; v25=[d[2] for d in data]; cat=[d[3] for d in data]
x=np.arange(len(labels)); w=0.38

fig,ax=plt.subplots(figsize=(9.5,5))
ax.bar(x-w/2, v24, w, color=GREY, label="2024")
c25=[ORANGE if c=="indo" else (NAVY if c=="eu" else TEAL) for c in cat]
ax.bar(x+w/2, v25, w, color=c25, label="2025")
for xi,(a,b) in enumerate(zip(v24,v25)):
    ax.annotate(f"{a:g}%",(xi-w/2,a),xytext=(0,3),textcoords="offset points",ha="center",fontsize=8,color="#475569")
    ax.annotate(f"{b:g}%",(xi+w/2,b),xytext=(0,3),textcoords="offset points",ha="center",fontsize=8.5,fontweight="bold",color=NAVY)
ax.set_xticks(x); ax.set_xticklabels(labels,fontsize=10)
ax.set_ylabel("Pangsa penjualan mobil listrik (%)")
ax.set_title("Pangsa Penjualan Mobil Listrik (EV): Indonesia vs ASEAN vs Uni Eropa",
             fontsize=12.5,fontweight="bold",color=NAVY)
ax.legend(loc="upper right",fontsize=9,title="Tahun")
ax.spines[["top","right"]].set_visible(False); ax.grid(axis="y",alpha=.25); ax.set_ylim(0,45)
ax.annotate("Indonesia: pangsa rendah\ntapi tumbuh tercepat (>2x)",(4+w/2,15),xytext=(3.0,33),
            fontsize=8.5,color=ORANGE,fontweight="bold",arrowprops=dict(arrowstyle="->",color=ORANGE))
ax.annotate("Uni Eropa = tolok ukur\n(sudah bangun pelacakan baterai)",(1+w/2,27),xytext=(0.2,40),
            fontsize=8.5,color=NAVY,arrowprops=dict(arrowstyle="->",color=NAVY))
ax.text(0.99,-0.12,"Sumber: IEA Global EV Outlook 2026 (EV Data Explorer)",transform=ax.transAxes,
        ha="right",fontsize=7.5,color="#94a3b8")
fig.savefig(OUT/"viz_banding_asean_eu.png",dpi=150,bbox_inches="tight",facecolor="white")
print("OK viz_banding_asean_eu.png")
