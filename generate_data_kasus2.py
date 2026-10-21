import numpy as np
import pandas as pd

np.random.seed(42)
n_samples = 1000

# 1. Variabel Utama Kasus 2
jurusans = [
    'Sistem Informasi',
    'Manajemen',
    'Teknik Informatika',
    'Akuntansi',
    'Ilmu Komunikasi',
]
prob_jurusan = [0.3, 0.25, 0.2, 0.15, 0.1]

# 2. Generasi Data Sintetis
jurusan_list = np.random.choice(jurusans, size=n_samples, p=prob_jurusan)
semester_list = np.random.choice(
    list(range(1, 9)), size=n_samples, p=[0.2, 0.18, 0.15, 0.15, 0.12, 0.1, 0.06, 0.04]
)

# Usia disesuaikan rasional terhadap semester (Semester 1 sekitar 18-19, dst)
usia_list = [int(18 + (sem * 0.5) + np.random.choice([0, 1])) for sem in semester_list]

# IPK berdistribusi normal (rata-rata 3.25, standar deviasi 0.4, rentang 2.00 - 4.00)
ipk_raw = np.random.normal(loc=3.25, scale=0.4, size=n_samples)
ipk_list = np.clip(np.round(ipk_raw, 2), 2.00, 4.00)

# 3. Bentuk DataFrame
df_mhs = pd.DataFrame({
    'Jurusan': jurusan_list,
    'Semester': semester_list,
    'IPK': ipk_list,
    'Usia': usia_list,
})

# Simpan CSV
df_mhs.to_csv('dataset_profil_mahasiswa.csv', index=False)
print(
    "✅ Dataset 1.000 profil mahasiswa berhasil dibuat:"
    " 'dataset_profil_mahasiswa.csv'"
)