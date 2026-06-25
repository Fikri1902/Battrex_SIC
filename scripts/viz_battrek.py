"""
BATTREK — generator visualisasi untuk laporan komprehensif.
Menghasilkan: data deskriptif (populasi, pangsa pasar, komposisi, penjualan BEV)
+ 2 flow BATTREK (mikro-fitur & makro-ekosistem).
Sumber data: GAIKINDO/Kemenperin & SRUT Kemenhub (Bahan Dirjen ILMATE GIIAS, 31 Jul 2025).
Output PNG -> ../figures/
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

OUT = Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)
NAVY="#0f2c59"; TEAL="#0ea5e9"; GREEN="#16a34a"; ORANGE="#f59e0b"; RED="#dc2626"; GREY="#94a3b8"; LIGHT="#e2e8f0"

def save(fig, name):
    fig.savefig(OUT / name, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig); print("OK", name)

# ---------- 1. Populasi EV (line) ----------
pop = {2019:1437,2020:3894,2021:15883,2022:41743,2023:116439,2024:207478,2025:274802}
fig,ax=plt.subplots(figsize=(8,4.5))
xs=list(pop); ys=list(pop.values())
ax.plot(xs,ys,"-o",color=TEAL,lw=3,ms=7)
ax.fill_between(xs,ys,color=TEAL,alpha=0.15)
for x,y in pop.items():
    ax.annotate(f"{y:,}".replace(",","."),(x,y),textcoords="offset points",xytext=(0,9),
                ha="center",fontsize=8.5,fontweight="bold",color=NAVY)
ax.set_title("Populasi Kendaraan Listrik di Indonesia, 2019-2025",fontsize=13,fontweight="bold",color=NAVY)
ax.set_ylabel("Unit terdaftar"); ax.set_xlabel("Tahun")
ax.annotate("~176x dalam 6 tahun",(2021.5,200000),fontsize=10,color=RED,fontweight="bold")
ax.grid(alpha=.25); ax.spines[["top","right"]].set_visible(False)
ax.text(0.99,-0.16,"Sumber: SRUT Kemenhub (via Kemenperin), per 24 Jun 2025",transform=ax.transAxes,
        ha="right",fontsize=7.5,color=GREY)
save(fig,"viz_populasi_ev.png")

# ---------- 2. Market share powertrain (stacked) ----------
yrs=["2021","2022","2023","2024","Jan-Jun\n2025"]
ICE=[99.64,98.53,93.08,88.45,82.51]; HEV=[0.28,0.49,5.21,6.55,7.26]
PHEV=[0.00,0.00,0.01,0.01,0.46]; BEV=[0.08,0.99,1.70,4.99,9.77]
fig,ax=plt.subplots(figsize=(8.5,5))
x=np.arange(len(yrs)); w=0.6
ax.bar(x,ICE,w,label="ICE (bensin/diesel)",color=GREY)
ax.bar(x,HEV,w,bottom=ICE,label="HEV (hybrid)",color=ORANGE)
ax.bar(x,PHEV,w,bottom=np.array(ICE)+np.array(HEV),label="PHEV",color=GREEN)
ax.bar(x,BEV,w,bottom=np.array(ICE)+np.array(HEV)+np.array(PHEV),label="BEV (listrik penuh)",color=TEAL)
for i in range(len(yrs)):
    ax.annotate(f"BEV {BEV[i]:.2f}%",(i,100.6),ha="center",fontsize=8.5,fontweight="bold",color=TEAL)
ax.set_ylim(78,103); ax.set_xticks(x); ax.set_xticklabels(yrs)
ax.set_title("Pangsa Pasar Mobil Baru per Jenis Penggerak (zoom 78-100%)",fontsize=12.5,fontweight="bold",color=NAVY)
ax.set_ylabel("% penjualan"); ax.legend(fontsize=8,loc="lower left",ncol=2)
ax.spines[["top","right"]].set_visible(False)
ax.text(0.99,-0.13,"Sumber: GAIKINDO (via Kemenperin)",transform=ax.transAxes,ha="right",fontsize=7.5,color=GREY)
save(fig,"viz_market_share.png")

# ---------- 3. Komposisi populasi 2025 (donut) ----------
labels=["Motor listrik (R2)  196.051","Mobil penumpang (R4)  77.227","Lainnya (R3/bus/komersil)  1.524"]
sizes=[196051,77227,617+638+266+3]; cols=[TEAL,NAVY,GREY]
fig,ax=plt.subplots(figsize=(7.5,5))
ax.pie(sizes,labels=None,colors=cols,autopct=lambda p:f"{p:.1f}%",pctdistance=0.78,
       wedgeprops=dict(width=0.42,edgecolor="white"),textprops=dict(color="white",fontweight="bold",fontsize=10))
ax.legend(labels,loc="center left",bbox_to_anchor=(0.95,0.5),fontsize=9,frameon=False)
ax.text(0,0,"274.802\nunit EV\n(2025)",ha="center",va="center",fontsize=12,fontweight="bold",color=NAVY)
ax.set_title("Komposisi Populasi Kendaraan Listrik 2025",fontsize=13,fontweight="bold",color=NAVY)
save(fig,"viz_komposisi_2025.png")

# ---------- 4. Penjualan BEV mobil (bar) ----------
s={"2021":685,"2022":10327,"2023":17062,"2024":43194,"H1-2025":36611}
fig,ax=plt.subplots(figsize=(8,4.5))
bars=ax.bar(list(s),list(s.values()),color=TEAL,width=0.6)
bars[-1].set_color(ORANGE)
for b,v in zip(bars,s.values()):
    ax.annotate(f"{v:,}".replace(",","."),(b.get_x()+b.get_width()/2,v),textcoords="offset points",
                xytext=(0,4),ha="center",fontsize=9,fontweight="bold",color=NAVY)
ax.set_title("Penjualan Mobil Listrik (BEV) Indonesia",fontsize=13,fontweight="bold",color=NAVY)
ax.set_ylabel("Unit"); ax.spines[["top","right"]].set_visible(False); ax.grid(axis="y",alpha=.25)
ax.text(0.99,-0.15,"Sumber: GAIKINDO. *H1-2025 = Jan-Jun (baru separuh tahun)",transform=ax.transAxes,
        ha="right",fontsize=7.5,color=GREY)
save(fig,"viz_penjualan_bev.png")

# ---------- helper box & arrow ----------
def box(ax,x,y,w,h,text,fc,tc="white",fs=10):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle="round,pad=0.02,rounding_size=0.08",
                 facecolor=fc,edgecolor="white",linewidth=1.5))
    ax.text(x+w/2,y+h/2,text,ha="center",va="center",color=tc,fontsize=fs,fontweight="bold")
def arrow(ax,x1,y1,x2,y2,color=NAVY,style="-|>"):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle=style,mutation_scale=18,
                 color=color,lw=2,shrinkA=2,shrinkB=2))

# ---------- 5. Flow MIKRO (fitur BATTREK) ----------
fig,ax=plt.subplots(figsize=(14,5)); ax.set_xlim(0,14); ax.set_ylim(0,5); ax.axis("off")
ax.set_title("Alur Mikro - Cara Kerja Fitur BATTREK (siklus hidup satu baterai)",fontsize=13,fontweight="bold",color=NAVY)
box(ax,0.2,2.0,2.2,1.1,"1. Battery\nRegistry & ID",NAVY)
box(ax,2.9,2.0,2.2,1.1,"2. SoH Monitoring\n(ML)",TEAL)
box(ax,5.6,2.0,2.2,1.1,"3. Decision\nEngine (SoH)",ORANGE)
box(ax,8.6,3.1,2.5,1.0,"4. Second-Life\n70-80% -> BESS",GREEN,fs=9)
box(ax,8.6,0.9,2.5,1.0,"5. Recycling\n<70% -> Li/Co/Ni",RED,fs=9)
box(ax,11.6,2.0,2.2,1.1,"6. National\nDashboard",NAVY)
arrow(ax,2.4,2.55,2.9,2.55); arrow(ax,5.1,2.55,5.6,2.55)
arrow(ax,7.8,2.7,8.6,3.4); arrow(ax,7.8,2.4,8.6,1.5)
arrow(ax,11.1,3.6,11.7,2.9,color=GREEN); arrow(ax,11.1,1.4,11.7,2.2,color=RED)
ax.text(7,0.5,"umpan balik data -> registry & kebijakan",ha="center",fontsize=8,color=GREY,style="italic")
ax.text(0.2,4.4,">=80% SoH -> tetap dipakai di kendaraan (belum keluar sistem)",fontsize=9,color=NAVY)
save(fig,"battrek_flow_mikro.png")

# ---------- 6. Flow MAKRO (ekosistem) ----------
fig,ax=plt.subplots(figsize=(13,8.5)); ax.set_xlim(0,13); ax.set_ylim(0,9); ax.axis("off")
ax.set_title("Alur Makro - Ekosistem & Pemangku Kepentingan BATTREK",fontsize=14,fontweight="bold",color=NAVY)
box(ax,5.0,4.0,3.0,1.4,"BATTREK\nPlatform Nasional\n(registri + dashboard)",NAVY,fs=11)
box(ax,0.4,6.8,2.8,1.0,"Produsen / Importir\nbaterai & EV",TEAL,fs=9)
box(ax,0.4,1.2,2.8,1.0,"Pemilik EV + Bengkel/\nUji berkala",TEAL,fs=9)
box(ax,5.2,7.6,2.6,1.0,"Regulator\nESDM-KLHK-Kemenperin",ORANGE,fs=9)
box(ax,9.8,6.4,2.8,1.0,"Titik Pengumpulan\n(collection point)",GREY,fs=9)
box(ax,9.8,7.9,2.8,0.9,"Second-Life / PLN\nBESS pulau & EBT",GREEN,fs=9)
box(ax,9.8,1.4,2.8,1.0,"Daur Ulang /\nUrban Mining (Li/Co/Ni)",RED,fs=9)
box(ax,4.6,1.0,3.8,0.9,"Output: kesiapan ekspor +\nperencanaan fasilitas per provinsi",NAVY,fs=9)
arrow(ax,3.2,7.0,5.0,5.2,color=TEAL); ax.text(3.3,6.4,"daftar ID & kimia",fontsize=8,color=TEAL)
arrow(ax,3.2,1.7,5.0,4.2,color=TEAL); ax.text(3.3,2.8,"data SoH berkala",fontsize=8,color=TEAL)
arrow(ax,6.5,7.6,6.5,5.4,color=ORANGE,style="<|-|>"); ax.text(6.6,6.7,"kebijakan &\npengawasan",fontsize=8,color=ORANGE)
arrow(ax,8.0,4.9,9.8,6.8,color=NAVY); ax.text(8.1,6.0,"rute keputusan",fontsize=8,color=NAVY)
arrow(ax,11.2,6.4,11.2,7.9,color=GREEN)
arrow(ax,11.2,6.4,11.2,2.4,color=RED); ax.text(11.3,4.4,"<70%",fontsize=8,color=RED)
arrow(ax,6.5,4.0,6.5,1.9,color=NAVY)
ax.text(6.5,0.4,"Privacy-by-design: yang dilacak baterai (identitas & kesehatan), BUKAN lokasi pemilik",
        ha="center",fontsize=9,color=NAVY,style="italic")
save(fig,"battrek_flow_makro.png")

print("SELESAI semua figur.")
