import plotly.express as px
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dashboard Profil Mahasiswa", page_icon="🎓", layout="wide"
)


@st.cache_data
def load_data():
  return pd.read_csv("dataset_profil_mahasiswa.csv")


df = load_data()

st.title("🎓 Dashboard Analisis Profil Mahasiswa SABRINA SEPTIANANDA-241051026")
st.markdown("Analisis Komprehensif Dataset Mahasiswa (1.000 Data Sintetis)")
st.divider()

# Sidebar Filter
st.sidebar.header("Filter Data")
jurusan_opt = st.sidebar.multiselect(
    "Pilih Jurusan:",
    options=df["Jurusan"].unique(),
    default=df["Jurusan"].unique(),
)

sem_range = st.sidebar.slider(
    "Pilih Rentang Semester:",
    min_value=int(df["Semester"].min()),
    max_value=int(df["Semester"].max()),
    value=(int(df["Semester"].min()), int(df["Semester"].max())),
)

# Filter Dataset
df_filtered = df[
    (df["Jurusan"].isin(jurusan_opt))
    & (df["Semester"] >= sem_range[0])
    & (df["Semester"] <= sem_range[1])
]

# KPI Metrics
c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Mahasiswa", f"{len(df_filtered):,} Mhs")
c2.metric(
    "Rata-rata IPK",
    f"{df_filtered['IPK'].mean():.2f}" if len(df_filtered) > 0 else "0",
)
c3.metric(
    "Rata-rata Usia",
    f"{df_filtered['Usia'].mean():.1f} Tahun" if len(df_filtered) > 0 else "0",
)
c4.metric(
    "IPK Tertinggi",
    f"{df_filtered['IPK'].max():.2f}" if len(df_filtered) > 0 else "0",
)

st.divider()

# Visualisasi Baris 1: Nominal (Jurusan) & Ordinal (Semester)
row1_col1, row1_col2 = st.columns(2)

with row1_col1:
  st.subheader("📌 Jumlah Mahasiswa per Jurusan (Bar Chart Nominal)")
  jur_df = df_filtered["Jurusan"].value_counts().reset_index()
  jur_df.columns = ["Jurusan", "Jumlah"]
  fig_jur = px.bar(
      jur_df, x="Jurusan", y="Jumlah", color="Jurusan", text_auto=True
  )
  st.plotly_chart(fig_jur, use_container_width=True)

with row1_col2:
  st.subheader("📶 Distribusi Tingkat Semester (Bar Chart Ordinal)")
  sem_df = (
      df_filtered["Semester"]
      .value_counts()
      .reset_index()
      .sort_values("Semester")
  )
  sem_df.columns = ["Semester", "Jumlah"]
  fig_sem = px.bar(
      sem_df,
      x="Semester",
      y="Jumlah",
      color_discrete_sequence=["#2E86C1"],
      text_auto=True,
  )
  fig_sem.update_xaxes(dtick=1)
  st.plotly_chart(fig_sem, use_container_width=True)

# Visualisasi Baris 2: Kontinu (IPK & Usia)
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
  st.subheader("📊 Distribusi IPK (Histogram & Marginal Rug)")
  fig_ipk = px.histogram(
      df_filtered, x="IPK", nbins=25, color="Jurusan", marginal="rug"
  )
  st.plotly_chart(fig_ipk, use_container_width=True)

with row2_col2:
  st.subheader("📦 Sebaran IPK per Jurusan (Box Plot Outlier)")
  fig_box = px.box(
      df_filtered, x="Jurusan", y="IPK", color="Jurusan", points="all"
  )
  st.plotly_chart(fig_box, use_container_width=True)

with st.expander("📄 Lihat Dataset Profil Mahasiswa"):
  st.dataframe(df_filtered, use_container_width=True)