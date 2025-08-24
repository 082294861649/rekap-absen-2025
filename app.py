import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Rekap Absen Pegawai 2025", layout="wide")

st.title("📊 Rekap Absen Pegawai 2025")

# ====== CONFIG GOOGLE SHEETS ======
SHEET_ID = "1JG2Vn_qInZrF5OdOIT62L2gu0vqzkP84_WiQFlPDYMo"
SHEET_NAME = "Rekap_Absen"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

try:
    df = pd.read_csv(url)
    df = df.dropna(how="all")  # hapus baris kosong

    # Normalisasi header kolom
    df.columns = df.columns.str.strip()

    expected_cols = ["Tanggal", "Hari", "Nama", "Jam Masuk", "Jam Pulang"]
    if len(df.columns) >= 5:
        df = df.iloc[:, :5]
        df.columns = expected_cols

    # Konversi tanggal
    df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")

    st.subheader("📋 Data Absensi")
    st.dataframe(df)

    # Filter pegawai
    pegawai_list = ["-- Semua --"] + sorted(df["Nama"].dropna().unique().tolist())
    pegawai = st.selectbox("Pilih Pegawai", pegawai_list)

    if pegawai != "-- Semua --":
        df_filtered = df[df["Nama"] == pegawai]
    else:
        df_filtered = df

    st.subheader("📌 Rekap Kehadiran")
    hadir = df_filtered.groupby("Nama").size().reset_index(name="Jumlah Hadir")
    st.dataframe(hadir)

    # ====== Grafik per Bulan ======
    st.subheader("📈 Grafik Kehadiran Bulanan")
    df_filtered["Bulan"] = df_filtered["Tanggal"].dt.to_period("M")
    grafik = df_filtered.groupby(["Nama", "Bulan"]).size().reset_index(name="Jumlah Hadir")

    if pegawai != "-- Semua --":
        grafik = grafik[grafik["Nama"] == pegawai]

    fig, ax = plt.subplots(figsize=(8, 4))
    for nama in grafik["Nama"].unique():
        data = grafik[grafik["Nama"] == nama]
        ax.bar(data["Bulan"].astype(str), data["Jumlah Hadir"], label=nama)

    ax.set_xlabel("Bulan")
    ax.set_ylabel("Jumlah Kehadiran")
    ax.set_title("Grafik Kehadiran Bulanan")
    ax.legend()
    st.pyplot(fig)

except Exception as e:
    st.error(f"Gagal membaca file dari Google Sheets! \n\n{e}")
