import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

# Set Konfigurasi Halaman Streamlit
st.set_page_config(
    page_title="Dashboard Operasional Penjualan",
    page_icon="📊",
    layout="wide",
)


# Load Data (Gunakan caching untuk performa cepat)
@st.cache_data
def load_data():
  df = pd.read_csv("dataset_operasional_penjualan.csv")
  df["Tanggal"] = pd.to_datetime(df["Tanggal"])
  return df


df = load_data()

# Header Utama
st.title("📊 Dashboard Operasional Penjualan SABRINA SEPTIANANDA-241051026")
st.markdown(
    "Analisis Komprehensif Dataset Operasional Penjualan (1.000 Transaksi)"
)
st.divider()

# Sidebar - Filter Interaktif
st.sidebar.header("Filter Data")
kategori_option = st.sidebar.multiselect(
    "Pilih Kategori:",
    options=df["Kategori"].unique(),
    default=df["Kategori"].unique(),
)

# Filter Dataset berdasarkan Pilihan User
df_filtered = df[df["Kategori"].isin(kategori_option)]

# 1. Ringkasan KPI (Key Performance Indicators)
col1, col2, col3, col4 = st.columns(4)
total_revenue = df_filtered["Total Penjualan (Rp)"].sum()
total_qty = df_filtered["Jumlah Terjual"].sum()
total_tx = len(df_filtered)
avg_tx = (
    df_filtered["Total Penjualan (Rp)"].mean() if total_tx > 0 else 0
)

col1.metric("Total Pendapatan", f"Rp {total_revenue:,.0f}")
col2.metric("Total Produk Terjual", f"{total_qty:,} Unit")
col3.metric("Total Transaksi", f"{total_tx:,}")
col4.metric("Rata-rata / Transaksi", f"Rp {avg_tx:,.0f}")

st.divider()

# 2. Visualisasi Variabel Kategori & Numerik Diskrit
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
  st.subheader("📌 Penjualan per Kategori (Bar & Pie Chart)")
  kat_df = (
      df_filtered.groupby("Kategori")["Total Penjualan (Rp)"]
      .sum()
      .reset_index()
  )
  fig_pie = px.pie(
      kat_df,
      values="Total Penjualan (Rp)",
      names="Kategori",
      hole=0.4,
      color_discrete_sequence=px.colors.qualitative.Set2,
  )
  st.plotly_chart(fig_pie, use_container_width=True)

with row1_col2:
  st.subheader("📦 Top Produk Terlaris (Kuantitas Terjual)")
  prod_df = (
      df_filtered.groupby(["Produk", "Kategori"])["Jumlah Terjual"]
      .sum()
      .reset_index()
      .sort_values("Jumlah Terjual", ascending=True)
  )
  fig_bar = px.bar(
      prod_df,
      x="Jumlah Terjual",
      y="Produk",
      color="Kategori",
      orientation="h",
  )
  st.plotly_chart(fig_bar, use_container_width=True)

# 3. Visualisasi Distribusi Harga & Tren Waktu
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
  st.subheader("📈 Tren Pendapatan Harian (Line Chart)")
  trend_df = (
      df_filtered.groupby("Tanggal")["Total Penjualan (Rp)"]
      .sum()
      .reset_index()
  )
  fig_line = px.line(
      trend_df,
      x="Tanggal",
      y="Total Penjualan (Rp)",
      markers=False,
      line_shape="linear",
  )
  st.plotly_chart(fig_line, use_container_width=True)

with row2_col2:
  st.subheader("📊 Distribusi Harga Produk (Histogram)")
  fig_hist = px.histogram(
      df_filtered,
      x="Harga (Rp)",
      nbins=30,
      color="Kategori",
      marginal="rug",
  )
  st.plotly_chart(fig_hist, use_container_width=True)

# 4. Tabel Detail Data
with st.expander("📄 Lihat Detail Data Operasional"):
  st.dataframe(df_filtered, use_container_width=True)