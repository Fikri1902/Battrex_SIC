# BATTREK — Data & Reproducibility (SIC 2026)

Repositori ini berisi **data, kode, sumber, dan hasil** yang dipakai untuk infografis **BATTREK** (Statistics Infographics Competition / SATRIA DATA 2026, sub-tema *Transisi Energi dan Tantangan Industri Nasional*).

> **Tujuan repo ini:** memungkinkan **validasi & reproduksi**. Juri/pembaca dapat memeriksa data yang dipakai dan **menghasilkan ulang** seluruh angka & grafik infografis. (Laporan/deskripsi sengaja TIDAK disertakan di sini.)

**Ringkas isu:** booming kendaraan listrik (EV) Indonesia hari ini = "bom waktu" gelombang baterai bekas ~2030–2035 (baterai berumur 8–12 tahun). Semua perhitungan di bawah dapat direproduksi.

## Struktur folder
```
BATTREK_SIC_GITHUB/
├── data/        Data input & output olahan (xlsx, csv, json)
├── scripts/     Kode Python reproducible (model + visualisasi)
├── figures/     Grafik & peta hasil generate (PNG)
├── sources/     PDF sumber yang disitasi + SUMBER_DATA_LINKS.md (tautan unduh)
└── README.md
```

## Data input & sumbernya
| Berkas di `data/` | Isi | Sumber asli |
|---|---|---|
| `EV Data Explorer 2026.xlsx` | Penjualan/stok/pangsa EV antarnegara (historis) | IEA Global EV Outlook 2026 — tautan unduh di `sources/SUMBER_DATA_LINKS.md` |
| `SPKLU_Rekap_dan_Kategori_Wilayah.xlsx` | SPKLU per provinsi 2023–2030 + kategori wilayah | Transkripsi dari `sources/Kepmen_ESDM_Rencana_Pengembangan_SPKLU_2025_2030.pdf` |
| `battrek_decrement_output.json` | Output proyeksi gelombang akhir-hidup | dihasilkan `scripts/model_decrement_battrek.py` |
| `battrek_cluster_provinsi.csv` / `.json` | Output clustering provinsi | dihasilkan `scripts/cluster_provinsi_battrek.py` |

Angka penjualan mobil BEV (GAIKINDO) dan populasi EV (SRUT Kemenhub) yang dipakai model di-*hardcode* di dalam script (sumber dikomentari), berasal dari `sources/Kemenperin_Bahan_Dirjen_ILMATE_Seminar_GIIAS_2025.pdf` dan `sources/Kemenperin_Bahan_Perindustrian_Populasi_Kendaraan_Listrik.pdf`.

## Cara mereproduksi
**Prasyarat:** Python 3.10+ dan paket:
```
pip install numpy pandas openpyxl scikit-learn matplotlib
```
Jalankan dari folder `scripts/`. Output otomatis tertulis ke `../data/` dan `../figures/` (sudah relatif terhadap repo ini). **Urutan disarankan** (script 3 & 4 memakai output script 1 & 2):
```
python model_decrement_battrek.py     # -> data/battrek_decrement_output.json  (proyeksi gelombang akhir-hidup)
python cluster_provinsi_battrek.py     # -> data/battrek_cluster_provinsi.csv/.json + figures/peta_cluster_provinsi.png
python grafik_gelombang.py             # -> figures/grafik_gelombang_eol.png
python viz_battrek.py                  # -> figures/viz_*.png, battrek_flow_*.png, mockup_dashboard_battrek.png
python viz_banding.py                  # -> figures/viz_banding_asean_eu.png
```
> `cluster_provinsi_battrek.py` mengunduh GeoJSON batas provinsi dari internet (butuh koneksi). Telah diuji: kelima script berjalan dari dalam repo ini dan menghasilkan ulang seluruh `data/` & `figures/`.

## Metode (ringkas)
- **Model decrement / kohort–survival** (Weibull, alpha=3,5; umur baterai 8/10/12 thn) — kalibrasi Hadinata dkk. (2025). Mengubah deret penjualan → proyeksi baterai akhir-hidup. Skenario *committed* (armada yang sudah terjual) & *pertumbuhan* (anchor proyeksi ESDM).
- **Clustering K-Means** (k=4; silhouette 0,472) atas SPKLU per provinsi 2024 & 2030 → segmentasi paparan ekosistem EV (peta 4 tier).
- **Visualisasi deskriptif** dari data resmi (populasi SRUT, pangsa GAIKINDO, perbandingan IEA).

## Sumber data (URL lengkap di `sources/SUMBER_DATA_LINKS.md`)
| Data | Sumber |
|---|---|
| Penjualan mobil BEV per powertrain 2021–H1 2025 | GAIKINDO via Kemenperin (Bahan Dirjen ILMATE, GIIAS 2025) |
| Populasi EV terdaftar 2019–2025 (274.802) | SRUT Kementerian Perhubungan |
| SPKLU & KBLBB per provinsi 2024–2030 | Kepmen ESDM No. 24.K/TL.01/MEM.L/2025 |
| Penjualan/stok EV historis + pangsa internasional | IEA Global EV Outlook 2026 (EV Data Explorer) |
| Parameter umur/kapasitas baterai & metode | Hadinata dkk. (2025); Jiang dkk. (2021) |
| Acuan regulasi paspor baterai | Regulation (EU) 2023/1542 |

## Angka kunci yang dihasilkan
- **Committed fleet:** ~134.098 baterai mobil (~6 GWh) akhir-hidup s.d. 2035, puncak ~22.558/tahun pada 2032.
- **Skenario pertumbuhan (anchor ESDM):** ~1,37 juta unit (~75,6 GWh) s.d. 2040.
- **Spasial:** 7 provinsi "episentrum" (DKI, Jabar, Jatim, Jateng, Bali, Sumut, Banten).

## Keterbatasan
Proyeksi inti dibatasi mobil BEV (motor = ekstensi); penjualan 2025 disetahunkan dari semester I; SPKLU dipakai sebagai *proxy* sebaran EV per provinsi; parameter baterai mengutip literatur.

*Tanpa identitas peserta sesuai aturan lomba. Tahun & sumber dicantumkan pada setiap angka.*
