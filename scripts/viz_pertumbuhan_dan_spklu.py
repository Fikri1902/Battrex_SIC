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

# ---------- 1. Lonjakan pangsa pasar EV 2024->2025 ----------
# (negara, share 2024 %, share 2025 %) -- IEA EV sales share, Cars
share=[("Vietnam",19,40),("Singapura",34,37),("Uni Eropa",21,27),("Thailand",13,23),
       ("Indonesia",6.8,15),("Filipina",1.3,10),("Malaysia",3.1,7)]
labels=[s[0] for s in share]; v24=[s[1] for s in share]; v25=[s[2] for s in share]
inc=[(b-a)/a*100 for a,b in zip(v24,v25)]
x=np.arange(len(labels)); w=0.38
fig,ax=plt.subplots(figsize=(10,5.2))
ax.bar(x-w/2,v24,w,color=GREY,label="2024")
c25=[ORANGE if l=="Indonesia" else (NAVY if l=="Uni Eropa" else TEAL) for l in labels]
ax.bar(x+w/2,v25,w,color=c25,label="2025")
for i in range(len(labels)):
    ax.annotate(f"+{inc[i]:.0f}%",(i,max(v24[i],v25[i])),xytext=(0,4),textcoords="offset points",
                ha="center",fontsize=8.5,fontweight="bold",color=RED)
ax.set_xticks(x); ax.set_xticklabels(labels,fontsize=9.5)
ax.set_ylabel("Pangsa pasar mobil listrik (%)")
ax.set_title("Lonjakan Pangsa Pasar Mobil Listrik (EV) 2024 -> 2025",fontsize=13,fontweight="bold",color=NAVY)
ax.legend(loc="upper right",fontsize=9,title="Tahun")
ax.spines[["top","right"]].set_visible(False); ax.grid(axis="y",alpha=.25)
idx=labels.index("Indonesia")
ax.annotate("Indonesia: pangsa\nLEBIH DARI 2x lipat",(idx+w/2,15),xytext=(idx-1.2,30),
            fontsize=9,color=ORANGE,fontweight="bold",arrowprops=dict(arrowstyle="->",color=ORANGE))
ax.text(0.99,-0.12,"Sumber: IEA Global EV Outlook 2026. (Filipina +669% dari basis sangat kecil.)",
        transform=ax.transAxes,ha="right",fontsize=7.5,color="#94a3b8")
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
