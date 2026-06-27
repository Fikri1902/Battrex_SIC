"""
BATTREX — Pilar 3: Clustering Provinsi (paparan & kesiapan ekosistem EV)
========================================================================
Segmentasi 34 provinsi berdasarkan skala & lintasan infrastruktur SPKLU
(proxy resmi sebaran EV; SPKLU dialokasikan per kepadatan ekosistem EV,
rasio 5:1 Jabodetabek / 12:1 luar — Kepmen ESDM 24.K/TL.01/MEM.L/2025).

Data: SPKLU per provinsi 2024 & proyeksi 2030 (Tabel 1.1 Kepmen ESDM).
Divalidasi vs total region resmi (5/6 region persis; total nasional 2024=3163, 2030=62918).

Fitur clustering: log10(SPKLU2030) [skala] + log10(rasio pertumbuhan 2024->2030) [lintasan].
Metode: K-Means (standardisasi); k dipilih via silhouette (k=3..5).
Output: CSV + JSON cluster -> ../data/ ; peta choropleth PNG (best-effort).
"""
import json, urllib.request, math
from pathlib import Path
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# provinsi: [SPKLU 2024, SPKLU 2030]  (Kepmen ESDM, Tabel 1.1)
SPKLU = {
 'Aceh':[28,188],'Sumatera Utara':[136,1672],'Sumatera Barat':[39,438],'Riau':[36,396],
 'Jambi':[16,238],'Sumatera Selatan':[100,575],'Bengkulu':[16,120],'Lampung':[57,450],
 'Kepulauan Bangka Belitung':[24,207],'Kepulauan Riau':[7,542],
 'DKI Jakarta':[520,32589],'Jawa Barat':[821,6467],'Jawa Tengah':[216,2988],
 'DI Yogyakarta':[33,1929],'Jawa Timur':[155,5143],'Banten':[188,1519],
 'Bali':[263,2681],'Nusa Tenggara Barat':[27,352],'Nusa Tenggara Timur':[24,109],
 'Kalimantan Barat':[42,462],'Kalimantan Tengah':[24,75],'Kalimantan Selatan':[32,556],
 'Kalimantan Timur':[91,769],'Kalimantan Utara':[3,95],
 'Sulawesi Utara':[32,320],'Sulawesi Tengah':[32,111],'Sulawesi Selatan':[79,1255],
 'Sulawesi Tenggara':[32,157],'Gorontalo':[20,124],'Sulawesi Barat':[3,21],
 'Maluku':[27,114],'Maluku Utara':[16,118],'Papua Barat':[13,68],'Papua':[17,85],
}

prov = list(SPKLU.keys())
s24 = np.array([SPKLU[p][0] for p in prov], float)
s30 = np.array([SPKLU[p][1] for p in prov], float)
growth = s30 / np.maximum(s24, 1)
X = np.column_stack([np.log10(s30), np.log10(np.maximum(s24, 1.0))])  # scale-led (skala 2024 & 2030); rasio tumbuh dilaporkan terpisah
Xs = StandardScaler().fit_transform(X)

# pilih k via silhouette
best = None
for k in [3, 4, 5]:
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(Xs)
    sil = silhouette_score(Xs, km.labels_)
    print(f"k={k}  silhouette={sil:.3f}")
    if best is None or sil > best[1]:
        best = (k, sil, km)
k, sil, km = best
labels = km.labels_
print(f"\n-> dipilih k={k} (silhouette={sil:.3f})\n")

# urutkan label cluster berdasarkan rata-rata SPKLU2030 (besar->kecil) utk penamaan
order = sorted(range(k), key=lambda c: -s30[labels == c].mean())
rank = {c: i for i, c in enumerate(order)}
NAMA = ['Episentrum','Pertumbuhan Tinggi','Menengah','Rendah','Sangat Rendah']

rows = []
for i, p in enumerate(prov):
    tier = rank[labels[i]]
    rows.append({'provinsi': p, 'spklu_2024': int(s24[i]), 'spklu_2030': int(s30[i]),
                 'rasio_tumbuh': round(growth[i], 1), 'cluster': tier,
                 'cluster_nama': NAMA[tier]})

rows.sort(key=lambda r: (r['cluster'], -r['spklu_2030']))
print(f"{'Provinsi':28} {'SPKLU24':>8} {'SPKLU30':>8} {'x':>6}  Cluster")
for r in rows:
    print(f"{r['provinsi']:28} {r['spklu_2024']:>8} {r['spklu_2030']:>8} "
          f"{r['rasio_tumbuh']:>5}x  [{r['cluster']}] {r['cluster_nama']}")

print("\n--- KARAKTERISTIK CLUSTER ---")
summary = {}
for tier in range(k):
    members = [r for r in rows if r['cluster'] == tier]
    if not members: continue
    avg30 = np.mean([m['spklu_2030'] for m in members])
    avgg = np.mean([m['rasio_tumbuh'] for m in members])
    summary[NAMA[tier]] = {'n': len(members), 'rata_spklu_2030': round(avg30),
                           'rata_rasio_tumbuh': round(avgg, 1),
                           'anggota': [m['provinsi'] for m in members]}
    print(f"[{tier}] {NAMA[tier]:18} n={len(members):2}  rata SPKLU2030={avg30:>7.0f}  "
          f"rata tumbuh={avgg:.1f}x")
    print(f"      {', '.join(m['provinsi'] for m in members)}")

# simpan
outdir = Path(__file__).resolve().parent.parent / "data"
outdir.mkdir(parents=True, exist_ok=True)
(outdir / "battrek_cluster_provinsi.json").write_text(
    json.dumps({'k': k, 'silhouette': round(sil, 3), 'rows': rows, 'summary': summary},
               indent=2, ensure_ascii=False), encoding="utf-8")
import csv
with open(outdir / "battrek_cluster_provinsi.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=['provinsi','spklu_2024','spklu_2030','rasio_tumbuh','cluster','cluster_nama'])
    w.writeheader(); w.writerows(rows)
print(f"\nTersimpan: {outdir/'battrek_cluster_provinsi.csv'}")

# ---- PETA (best-effort) ----------------------------------------------------
print("\n--- Coba render peta choropleth ---")
try:
    import subprocess, sys
    try:
        import matplotlib
    except ImportError:
        subprocess.run([sys.executable,'-m','pip','install','-q','matplotlib'])
        import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Polygon as MplPoly

    url = "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia-province.json"
    gj = json.loads(urllib.request.urlopen(url, timeout=60).read().decode())
    feats = gj['features']
    print("GeoJSON features:", len(feats), "| contoh properti:", list(feats[0]['properties'].keys()))

    def norm(s):
        s = s.upper().replace('PROVINSI','').replace('DAERAH KHUSUS IBUKOTA','DKI')
        s = s.replace('DAERAH ISTIMEWA','DI').replace('.', '').strip()
        return ' '.join(s.split())
    tier_by_norm = {norm(r['provinsi']): r['cluster'] for r in rows}
    alias = {'JAKARTA RAYA':'DKI JAKARTA','YOGYAKARTA':'DI YOGYAKARTA',
             'BANGKA BELITUNG':'KEPULAUAN BANGKA BELITUNG'}

    colors = {0:'#d11149',1:'#f17105',2:'#1a8fe3',3:'#06d6a0',4:'#cbd5e1'}  # 4 warna kontras per klaster (+abu utk tak terpetakan)
    fig, ax = plt.subplots(figsize=(14,6))
    matched, unmatched = 0, []
    for ft in feats:
        props = ft['properties']
        nm = ''
        for key in ['Propinsi','provinsi','name','NAME_1','state','PROVINSI']:
            if key in props and props[key]:
                nm = props[key]; break
        n = norm(nm); n = alias.get(n, n)
        tier = tier_by_norm.get(n)
        if tier is None:
            for kk, vv in tier_by_norm.items():
                if kk and (kk in n or n in kk):
                    tier = vv; break
        col = colors.get(tier, '#dddddd')
        if tier is None: unmatched.append(nm)
        else: matched += 1
        geom = ft['geometry']
        if geom['type'] == 'Polygon':
            rings = geom['coordinates']
        elif geom['type'] == 'MultiPolygon':
            rings = [r for poly in geom['coordinates'] for r in poly]
        else:
            rings = []
        for ring in rings:
            pts = np.array(ring, dtype=float)[:, :2]   # buang koordinat-Z bila ada
            ax.add_patch(MplPoly(pts, closed=True, facecolor=col,
                                 edgecolor='white', linewidth=0.3))
    ax.autoscale(); ax.set_aspect('equal'); ax.axis('off')
    ax.set_title('BATTREX — Klaster Provinsi: Tingkat Paparan Ekosistem EV',
                 fontsize=14, fontweight='bold', color='#0f2c59')
    from matplotlib.patches import Patch
    leg = [Patch(facecolor=colors.get(t, '#cbd5e1'), edgecolor='white',
                 label=f"{NAMA[t]} ({len([r for r in rows if r['cluster']==t])} provinsi)")
           for t in range(k)]
    ax.legend(handles=leg, title='Kategori klaster (warna)', loc='lower left',
              fontsize=10, title_fontsize=11, frameon=True, framealpha=0.95)
    print(f"Provinsi tercocokkan: {matched}/{len(feats)} | tak cocok: {unmatched}")
    mapdir = Path(__file__).resolve().parent.parent / "figures"
    mapdir.mkdir(parents=True, exist_ok=True)
    fig.savefig(mapdir / "peta_cluster_provinsi.png", dpi=150, bbox_inches='tight')
    print(f"Peta tersimpan: {mapdir/'peta_cluster_provinsi.png'}")
except Exception as e:
    print("Render peta gagal (lanjut tanpa peta):", repr(e))
