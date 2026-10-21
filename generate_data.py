import numpy as np
import pandas as pd

# 1. Menentukan seed agar hasil acak konsisten
np.random.seed(42)

# 2. Pemetaan Produk, Kategori, dan Rentang Harga
produk_data = {
    'Laptop': ('Elektronik', 7500000, 15000000),
    'Smartphone': ('Elektronik', 2500000, 8000000),
    'Headphone': ('Elektronik', 300000, 1500000),
    'Buku': ('Pendidikan', 45000, 150000),
    'Modul Kursus': ('Pendidikan', 100000, 500000),
    'Alat Tulis': ('Pendidikan', 10000, 50000),
    'Kemeja': ('Fashion', 150000, 400000),
    'Sepatu': ('Fashion', 300000, 1200000),
}

list_produk = list(produk_data.keys())
n_samples = 1000

# 3. Generasi 1000 Data Sintetis
pilihan_produk = np.random.choice(list_produk, size=n_samples)

kategori_list = []
harga_list = []
jumlah_terjual_list = []

for prod in pilihan_produk:
  kat, h_min, h_max = produk_data[prod]
  kategori_list.append(kat)
  harga_list.append(int(np.random.uniform(h_min, h_max)))

  # Kuantitas penjualan disesuaikan dengan tipe produk
  if kat == 'Elektronik':
    jumlah_terjual_list.append(np.random.randint(1, 15))
  elif kat == 'Pendidikan':
    jumlah_terjual_list.append(np.random.randint(10, 150))
  else:
    jumlah_terjual_list.append(np.random.randint(5, 50))

# Rentang tanggal dari 2024-01-01 s.d. 2024-12-31
tanggal_list = pd.date_range(
    start='2024-01-01', periods=n_samples, freq='D'
).take(np.random.randint(0, 365, n_samples))

# Membentuk DataFrame
df = pd.DataFrame({
    'Tanggal': tanggal_list,
    'Produk': pilihan_produk,
    'Kategori': kategori_list,
    'Harga (Rp)': harga_list,
    'Jumlah Terjual': jumlah_terjual_list,
})

df['Total Penjualan (Rp)'] = df['Harga (Rp)'] * df['Jumlah Terjual']
df = df.sort_values('Tanggal').reset_index(drop=True)

# Simpan ke CSV untuk digunakan di Streamlit
df.to_csv('dataset_operasional_penjualan.csv', index=False)

# 4. Ringkasan Analisis Data
print('--- RINGKASAN STATISTIK DATASET ---')
print(df.describe())

print('\n--- TOTAL PENJUALAN PER KATEGORI ---')
print(
    df.groupby('Kategori')[['Jumlah Terjual', 'Total Penjualan (Rp)']].sum()
)