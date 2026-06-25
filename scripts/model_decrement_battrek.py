"""
BATTREK — Model Decrement / Kohort-Survival Gelombang Limbah Baterai EV Indonesia
=================================================================================
Pass-1 build. Kalibrasi parameter dari Hadinata dkk. (2025),
"Electric Car Battery Waste in Indonesia", DOI 10.13170/aijst.14.1.43071,
yang mengadaptasi model Jiang dkk. (2021).

Metode:
  B(t) = Σ_s  Sales_s × [F(t-s) − F(t-s-1)]
  F(a) = 1 − exp(−(a/β)^α)          # Weibull CDF, fraksi pensiun pd umur a
  α (shape) = 3.5                    # Hadinata/Jiang
  β (umur baterai) = 8 thn (dijual ≤2030), 10 (2031-35), 12 (2036-40)
  Kapasitas BEV (Wh): 40k(≤2024) 50k(2025-29) 60k(2030-34) 80k(2035-39) 100k(2040)

Data penjualan (SALES/penambahan per tahun):
  - Historis BEV mobil Indonesia 2019-2025 = IEA Global EV Outlook 2026
    (EV Data Explorer; parameter 'EV sales', mode 'Cars', powertrain 'BEV').
  - Skenario masa depan 2026-2030 = penambahan tahunan dari proyeksi RESMI
    ESDM (Kepmen 24.K/TL.01/MEM.L/2025): ΔKBLBB stok.

Output: cetak tabel + simpan JSON ke ../data/battrek_decrement_output.json
Catatan: berat/ton material TIDAK dihitung di sini (dikutip dari Hadinata);
fokus pass-1 = UNIT & GWh. Motor listrik = ekstensi terpisah (asumsi beda).
"""

import json
import math
from pathlib import Path

ALPHA = 3.5  # Weibull shape (Hadinata 2025)

def beta_life(sale_year: int) -> float:
    if sale_year <= 2030:
        return 8.0
    elif sale_year <= 2035:
        return 10.0
    return 12.0

def cap_wh_bev(sale_year: int) -> float:
    if sale_year <= 2024:
        return 40_000.0
    elif sale_year <= 2029:
        return 50_000.0
    elif sale_year <= 2034:
        return 60_000.0
    elif sale_year <= 2039:
        return 80_000.0
    return 100_000.0

def F(age: float, beta: float) -> float:
    """Weibull CDF: fraksi kumulatif baterai pensiun pada umur `age`."""
    if age <= 0:
        return 0.0
    return 1.0 - math.exp(-((age / beta) ** ALPHA))

# --- Data penjualan BEV mobil (unit) ---------------------------------------
# Historis BEV mobil: GAIKINDO via Kemenperin (Bahan Dirjen ILMATE, Seminar GIIAS 31 Jul 2025).
# 2021-2024 = aktual; 2025 = 2x H1 (H1-2025 aktual 36.611 -> disetahunkan = 73.222).
# 2019-2020 dari IEA (sangat kecil, pengaruh ke gelombang ~nol).
sales_hist = {2019: 29, 2020: 340, 2021: 685, 2022: 10_327,
              2023: 17_062, 2024: 43_194, 2025: 73_222}

# Skenario masa depan (penambahan/tahun) dari proyeksi resmi ESDM ΔKBLBB
# stok: 2025=98.764 →2026=163.764 →…→2030=943.764
sales_esdm_future = {2026: 65_000, 2027: 80_000, 2028: 150_000,
                     2029: 240_000, 2030: 310_000}
# 2031-2040: pertahankan level 2030 (asumsi konservatif; ditandai sebagai batas bawah)
for y in range(2031, 2041):
    sales_esdm_future[y] = 310_000

def project(sales: dict, start=2025, end=2040):
    """Hitung unit & GWh baterai pensiun per tahun dari kumpulan kohort `sales`."""
    annual_units, annual_gwh = {}, {}
    for t in range(start, end + 1):
        u = 0.0
        g = 0.0
        for s, n in sales.items():
            if s > t:
                continue
            beta = beta_life(s)
            age = t - s
            frac = F(age, beta) - F(age - 1, beta)  # pensiun pada umur ini
            retired = n * frac
            u += retired
            g += retired * cap_wh_bev(s) / 1e9  # Wh → GWh
        annual_units[t] = u
        annual_gwh[t] = g
    # kumulatif
    cum_u, cum_g, cu, cg = {}, {}, 0.0, 0.0
    for t in range(start, end + 1):
        cu += annual_units[t]; cg += annual_gwh[t]
        cum_u[t] = cu; cum_g[t] = cg
    return annual_units, annual_gwh, cum_u, cum_g

def fmt(d):
    return {k: round(v, 1) for k, v in d.items()}

# Skenario A — COMMITTED FLEET (hanya yang SUDAH terjual s.d. 2025)
au_c, ag_c, cu_c, cg_c = project(sales_hist)

# Skenario B — + masa depan anchor ESDM
sales_full = {**sales_hist, **sales_esdm_future}
au_f, ag_f, cu_f, cg_f = project(sales_full)

print("=" * 70)
print("SKENARIO A — COMMITTED FLEET (mobil BEV yg SUDAH terjual s.d. 2025)")
print("  'Bahkan jika penjualan berhenti hari ini, baterai ini pasti pensiun.'")
print("=" * 70)
print(f"{'Thn':>5} | {'Pensiun/thn':>12} | {'Kumulatif':>12} | {'GWh/thn':>8} | {'GWh kum':>8}")
for t in range(2025, 2041):
    print(f"{t:>5} | {au_c[t]:>12,.0f} | {cu_c[t]:>12,.0f} | {ag_c[t]:>8.2f} | {cg_c[t]:>8.2f}")

print()
print("=" * 70)
print("SKENARIO B — + penjualan masa depan (anchor proyeksi resmi ESDM)")
print("=" * 70)
print(f"{'Thn':>5} | {'Pensiun/thn':>12} | {'Kumulatif':>12} | {'GWh/thn':>8} | {'GWh kum':>8}")
for t in range(2025, 2041):
    print(f"{t:>5} | {au_f[t]:>12,.0f} | {cu_f[t]:>12,.0f} | {ag_f[t]:>8.2f} | {cg_f[t]:>8.2f}")

# Hero numbers ringkas
print("\n--- HERO NUMBERS (ringkas) ---")
print(f"Committed: kumulatif baterai pensiun s.d. 2035 = {cu_c[2035]:,.0f} unit ({cg_c[2035]:.1f} GWh)")
print(f"Committed: puncak tahunan = {max(au_c.values()):,.0f} unit "
      f"(thn { max(au_c, key=au_c.get) })")
print(f"Skenario ESDM: kumulatif s.d. 2040 = {cu_f[2040]:,.0f} unit ({cg_f[2040]:.1f} GWh)")
print(f"Validasi vs Hadinata 2040 kum (LAS 6,2jt–HAS 9,8jt unit): "
      f"angka kita lebih kecil krn skenario penjualan konservatif (310rb/thn pasca-2030).")

# Simpan JSON
out = {
    "meta": {
        "model": "kohort-survival Weibull (decrement)",
        "kalibrasi": "Hadinata dkk. 2025 (DOI 10.13170/aijst.14.1.43071); Jiang dkk. 2021",
        "alpha_shape": ALPHA,
        "beta_umur_baterai": {"<=2030": 8, "2031-2035": 10, "2036-2040": 12},
        "kapasitas_bev_wh": {"<=2024": 40000, "2025-2029": 50000, "2030-2034": 60000,
                              "2035-2039": 80000, "2040": 100000},
        "sumber_penjualan": "Historis IEA EV Data Explorer 2026; proyeksi ESDM Kepmen 24.K/TL.01/MEM.L/2025",
        "catatan": "Pass-1. Mobil BEV saja. Berat/ton dikutip Hadinata, tidak dihitung ulang.",
    },
    "skenario_A_committed": {
        "unit_per_tahun": fmt(au_c), "unit_kumulatif": fmt(cu_c),
        "gwh_per_tahun": fmt(ag_c), "gwh_kumulatif": fmt(cg_c),
    },
    "skenario_B_esdm": {
        "unit_per_tahun": fmt(au_f), "unit_kumulatif": fmt(cu_f),
        "gwh_per_tahun": fmt(ag_f), "gwh_kumulatif": fmt(cg_f),
    },
}
out_path = Path(__file__).resolve().parent.parent / "data" / "battrek_decrement_output.json"
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"\nTersimpan: {out_path}")
