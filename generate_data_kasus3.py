import numpy as np
import pandas as pd

# Set seed agar hasil acak konsisten
np.random.seed(42)
n_samples = 1000

# 1. Definisi Kota dan Karakteristik Iklimnya
kota_data = {
    'Jakarta': {
        'suhu_mean': 31.5,
        'suhu_std': 2.0,
        'kelembaban_mean': 75,
        'kelembaban_std': 8,
    },
    'Bandung': {
        'suhu_mean': 23.5,
        'suhu_std': 2.5,
        'kelembaban_mean': 85,
        'kelembaban_std': 6,
    },
    'Surabaya': {
        'suhu_mean': 33.0,
        'suhu_std': 1.8,
        'kelembaban_mean': 70,
        'kelembaban_std': 9,
    },
    'Medan': {
        'suhu_mean': 29.0,
        'suhu_std': 2.2,
        'kelembaban_mean': 80,
        'kelembaban_std': 7,
    },
    'Yogyakarta': {
        'suhu_mean': 28.0,
        'suhu_std': 2.0,
        'kelembaban_mean': 78,
        'kelembaban_std': 8,
    },
}

list_kota = list(kota_data.keys())
pilihan_kota = np.random.choice(
    list_kota, size=n_samples, p=[0.25, 0.25, 0.2, 0.15, 0.15]
)

suhu_list = []
kelembaban_list = []
kondisi_list = []

# 2. Generasi Data Realistis Berdasarkan Kota
for kota in pilihan_kota:
  cfg = kota_data[kota]

  # Generate Suhu (°C) - Numerik Interval
  suhu = round(np.random.normal(cfg['suhu_mean'], cfg['suhu_std']), 1)

  # Generate Kelembaban (%) - Numerik Rasio
  kelembaban = int(
      np.clip(
          np.random.normal(cfg['kelembaban_mean'], cfg['kelembaban_std']),
          40,
          100,
      )
  )

  # Logika Penentuan Kondisi Cuaca berdasarkan Kelembaban dan Suhu
  if kelembaban >= 85:
    kondisi = np.random.choice(
        ['Hujan', 'Berawan', 'Badai'], p=[0.6, 0.3, 0.1]
    )
  elif kelembaban >= 75:
    kondisi = np.random.choice(
        ['Cerah Berawan', 'Berawan', 'Hujan'], p=[0.5, 0.35, 0.15]
    )
  else:
    kondisi = np.random.choice(['Cerah', 'Cerah Berawan'], p=[0.7, 0.3])

  suhu_list.append(suhu)
  kelembaban_list.append(kelembaban)
  kondisi_list.append(kondisi)

# Tanggal Pengamatan (1 Tahun)
tanggal_list = pd.date_range(
    start='2024-01-01', periods=n_samples, freq='D'
).take(np.random.randint(0, 365, n_samples))

# 3. Bentuk DataFrame
df_cuaca = pd.DataFrame({
    'Tanggal': tanggal_list,
    'Kota': pilihan_kota,
    'Suhu (°C)': suhu_list,
    'Kelembaban (%)': kelembaban_list,
    'Kondisi': kondisi_list,
})

df_cuaca = df_cuaca.sort_values('Tanggal').reset_index(drop=True)

# Simpan CSV
df_cuaca.to_csv('dataset_pengamatan_cuaca.csv', index=False)
print("✅ Dataset 1.000 data cuaca berhasil disimpan: 'dataset_pengamatan_cuaca.csv'")