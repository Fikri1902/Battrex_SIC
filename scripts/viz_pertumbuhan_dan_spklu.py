"""
BATTREK — 2 visualisasi tambahan (perbandingan internasional).
Sumber: IEA Global EV Outlook 2026 (EV Data Explorer) + dataset
'number of electric LDV per public charging point 2025' (IEA).
Output: ../figures/viz_pertumbuhan_pangsa.png, ../figures/viz_ev_per_spklu.png
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parent.parent / "figures"; OUT.mkdir(parents=True, exist_ok=True)
NAVY="#0f2c59"; TEAL="#0ea5e9"; ORANGE="#f59e0b"; GREY="#cbd5e1"; RED="#dc2626"

# ---------- 1. Kenaikan pangsa pasar EV 2024->2025 (1 bar/negara) ----------
# Set: pasar EV mapan (Indonesia, Thailand, Singapura, Uni Eropa). IEA EV sales share, Cars.
# bar = % kenaikan pangsa 2024->2025. Indonesia tertinggi pada set ini.
grow=[("Indonesia",6.8,15),("Thailand",13,23),("Uni Eropa",21,27),("Singapura",34,37)]
grow=[(n,(b-a)/a*100) for n,a,b in grow]
grow.sort(key=lambda t:-t[1])
labels=[g[0] for g in grow]; inc=[g[1] for g in grow]
cols=[ORANGE if l=="Indonesia" else (NAVY if l=="Uni Eropa" else TEAL) for l in labels]
fig,ax=plt.subplots(figsize=(9,5))
b=ax.bar(labels,inc,color=cols,width=0.6)
for bar,v in zip(b,inc):
    ax.annotate(f"+{v:.0f}%",(bar.get_x()+bar.get_width()/2,v),xytext=(0,4),
                textcoords="offset points",ha="center",fontsize=11,fontweight="bold",color=NAVY)
ax.set_ylabel("Kenaikan pangsa pasar mobil listrik 2024->2025 (%)")
ax.set_title("Indonesia: Lonjakan Pangsa Pasar Mobil Listrik Tertinggi\ndi antara Pasar EV Mapan ASEAN & Eropa",
             fontsize=13,fontweight="bold",color=NAVY)
ax.spines[["top","right"]].set_visible(False); ax.grid(axis="y",alpha=.25)
ax.set_ylim(0,max(inc)*1.18)
ax.text(0.99,-0.13,"Sumber: IEA Global EV Outlook 2026. Pangsa Indonesia 6,8% -> 15% (lebih dari 2x lipat). "
        "Set: pasar EV mapan; Vietnam/Malaysia/Filipina dikecualikan (basis kecil/baru).",
        transform=ax.transAxes,ha="right",fontsize=7,color="#94a3b8")
fig.savefig(OUT/"viz_pertumbuhan_pangsa.png",dpi=150,bbox_inches="tight",facecolor="white")
print("OK viz_pertumbuhan_pangsa.png")

# ---------- 2. EV per SPKLU (public charging point), 2025 ----------
# (negara, EV per 1 charging point) -- IEA 'Electric LDVs per charging point'
data=[("Filipina",130),("Singapura",42),("Indonesia",41),("Thailand",31),
      ("Malaysia",20),("Uni Eropa",13),("Vietnam",9),("Belanda",6)]
data=sorted(data,key=lambda t:t[1])  # asc -> horizontal bar bawah ke atas
lab=[d[0] for d in data]; val=[d[1] for d in data]
cols=[ORANGE if l=="Indonesia" else (NAVY if l in("Uni Eropa","Belanda") else TEAL) for l in lab]
fig,ax=plt.subplots(figsize=(9,5))
b=ax.barh(lab,val,color=cols)
for bar,v in zip(b,val):
    ax.annotate(f"{v:g}",(v,bar.get_y()+bar.get_height()/2),xytext=(4,0),textcoords="offset points",
                va="center",fontsize=9,fontweight="bold",color=NAVY)
ax.set_xlabel("Jumlah EV per 1 SPKLU (charging point umum)")
ax.set_title("Beban Charging: EV per 1 SPKLU, 2025\n(makin tinggi = makin sesak / kurang siap)",
             fontsize=12.5,fontweight="bold",color=NAVY)
ax.spines[["top","right"]].set_visible(False); ax.grid(axis="x",alpha=.25)
ax.text(0.99,-0.13,"Sumber: IEA (EV per public charging point, 2025). Belanda/UE = pembanding kawasan maju.",
        transform=ax.transAxes,ha="right",fontsize=7.5,color="#94a3b8")
fig.savefig(OUT/"viz_ev_per_spklu.png",dpi=150,bbox_inches="tight",facecolor="white")
print("OK viz_ev_per_spklu.png")
