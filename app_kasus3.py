import plotly.express as px
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard Pengamatan Cuaca", page_icon="🌤️", layout="wide"
)

@st.cache_data
def load_data():
  df = pd.read_csv("dataset_pengamatan_cuaca.csv")
  df["Tanggal"] = pd.to_datetime(df["Tanggal"])
  return df

df = load_data()

st.title("🌤️ Dashboard Analisis Pengamatan Cuaca SABRINA SEPTIANANDA-241051026")
st.markdown("Analisis Komprehensif Dataset Iklim & Cuaca (1.000 Data Sintetis)")
st.divider()

# Sidebar Filter
st.sidebar.header("Filter Data")
kota_opt = st.sidebar.multiselect(
    "Pilih Kota:", options=df["Kota"].unique(), default=df["Kota"].unique()
)

kondisi_opt = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca:",
    options=df["Kondisi"].unique(),
    default=df["Kondisi"].unique(),
)

# Filter Dataset
df_filtered = df[
    (df["Kota"].isin(kota_opt)) & (df["Kondisi"].isin(kondisi_opt))
]

# 1. Ringkasan KPI
c1, c2, c3, c4 = st.columns(4)
c1.metric(
    "Rata-rata Suhu",
    (
        f"{df_filtered['Suhu (°C)'].mean():.1f} °C"
        if len(df_filtered) > 0
        else "0 °C"
    ),
)
c2.metric(
    "Rata-rata Kelembaban",
    (
        f"{df_filtered['Kelembaban (%)'].mean():.1f} %"
        if len(df_filtered) > 0
        else "0 %"
    ),
)
c3.metric(
    "Suhu Maksimum",
    (
        f"{df_filtered['Suhu (°C)'].max():.1f} °C"
        if len(df_filtered) > 0
        else "0 °C"
    ),
)
c4.metric(
    "Suhu Minimum",
    (
        f"{df_filtered['Suhu (°C)'].min():.1f} °C"
        if len(df_filtered) > 0
        else "0 °C"
    ),
)

st.divider()

# 2. Visualisasi Baris 1: Nominal & Histogram Suhu (Interval)
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
  st.subheader("📌 Frekuensi Kondisi Cuaca (Bar Chart Nominal)")
  kond_df = df_filtered["Kondisi"].value_counts().reset_index()
  kond_df.columns = ["Kondisi", "Jumlah"]
  fig_kond = px.bar(
      kond_df,
      x="Kondisi",
      y="Jumlah",
      color="Kondisi",
      text_auto=True,
      color_discrete_sequence=px.colors.qualitative.Pastel,
  )
  st.plotly_chart(fig_kond, use_container_width=True)

with row1_col2:
  st.subheader("🌡️ Distribusi Suhu (°C) (Histogram Interval)")
  fig_suhu = px.histogram(
      df_filtered,
      x="Suhu (°C)",
      nbins=30,
      color="Kota",
      marginal="box",
      color_discrete_sequence=px.colors.qualitative.Set1,
  )
  st.plotly_chart(fig_suhu, use_container_width=True)

# 3. Visualisasi Baris 2: Kelembaban (Rasio) & Korelasi Suhu vs Kelembaban
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
  st.subheader("💧 Distribution Kelembaban (%) (Histogram Rasio)")
  fig_kelem = px.histogram(
      df_filtered,
      x="Kelembaban (%)",
      nbins=25,
      color="Kondisi",
      marginal="rug",
  )
  st.plotly_chart(fig_kelem, use_container_width=True)

with row2_col2:
  st.subheader("🔥 Korelasi Suhu vs Kelembaban (Scatter Plot)")
  fig_scat = px.scatter(
      df_filtered,
      x="Suhu (°C)",
      y="Kelembaban (%)",
      color="Kota",
      symbol="Kondisi",
      hover_data=["Tanggal"],
      opacity=0.7,
  )
  st.plotly_chart(fig_scat, use_container_width=True)

with st.expander("📄 Lihat Dataset Pengamatan Cuaca"):
  st.dataframe(df_filtered, use_container_width=True)