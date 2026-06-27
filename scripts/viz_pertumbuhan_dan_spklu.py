"""
BATTREX — 2 visualisasi tambahan (perbandingan internasional).
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

# ---------- 1b. Pangsa pasar 2024 vs 2025 — ASEAN + Eropa (grouped 2-bar) ----------
# Memperlihatkan KEADAAN tiap negara (level pangsa 2024 & 2025); Indonesia disorot;
# Uni Eropa ditandai "sudah punya regulasi". Urut menurun berdasarkan pangsa 2025.
allset=[("Indonesia",6.8,15),("Thailand",13,23),("Vietnam",19,40),("Singapura",34,37),
        ("Malaysia",3.1,7),("Filipina",1.3,10),("Uni Eropa",21,27)]
allset.sort(key=lambda t:-t[2])
labels=[g[0] for g in allset]; v24=[g[1] for g in allset]; v25=[g[2] for g in allset]
x=np.arange(len(labels)); w=0.40
fig,ax=plt.subplots(figsize=(11,5.4))
ax.bar(x-w/2,v24,w,color="#cbd5e1",label="2024")
c25=[ORANGE if l=="Indonesia" else (NAVY if l=="Uni Eropa" else TEAL) for l in labels]
ax.bar(x+w/2,v25,w,color=c25,label="2025")
for i in range(len(labels)):
    ax.annotate(f"{v24[i]:g}",(i-w/2,v24[i]),xytext=(0,3),textcoords="offset points",
                ha="center",fontsize=8,color="#64748b")
    ax.annotate(f"{v25[i]:g}",(i+w/2,v25[i]),xytext=(0,3),textcoords="offset points",
                ha="center",fontsize=8.5,fontweight="bold",color=NAVY)
ax.set_xticks(x); ax.set_xticklabels(labels,fontsize=10)
ax.set_ylabel("Pangsa pasar mobil listrik (%)")
ax.set_title("Keadaan Pasar Mobil Listrik: ASEAN & Uni Eropa (2024 vs 2025)",
             fontsize=13,fontweight="bold",color=NAVY)
ax.legend(loc="upper right",fontsize=9,title="Tahun")
ax.spines[["top","right"]].set_visible(False); ax.grid(axis="y",alpha=.25); ax.set_ylim(0,47)
idx=labels.index("Indonesia")
ax.annotate("Indonesia +121%\n(2x lipat dlm setahun)",(idx+w/2,v25[idx]),xytext=(idx-0.1,31),
            fontsize=9,color=ORANGE,fontweight="bold",ha="center",
            arrowprops=dict(arrowstyle="->",color=ORANGE))
eu=labels.index("Uni Eropa")
ax.annotate("sudah punya regulasi baterai\n(paspor baterai, Reg UE 2023/1542)",(eu+w/2,v25[eu]),
            xytext=(eu+0.15,43),fontsize=8.5,color=NAVY,ha="center",
            arrowprops=dict(arrowstyle="->",color=NAVY))
ax.text(0.99,-0.13,"Sumber: IEA Global EV Outlook 2026 (pangsa penjualan mobil listrik). Regulasi UE: Reg (EU) 2023/1542.",
        transform=ax.transAxes,ha="right",fontsize=7.5,color="#94a3b8")
fig.savefig(OUT/"viz_pertumbuhan_pangsa_asean.png",dpi=150,bbox_inches="tight",facecolor="white")
print("OK viz_pertumbuhan_pangsa_asean.png (2-bar)")

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
