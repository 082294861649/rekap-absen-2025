import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import urllib.parse

st.set_page_config(page_title="📊 Rekap Absen Pegawai 2025", layout="wide")

st.title("📊 Rekap Absen Pegawai 2025")

try:
    # ===== KONFIGURASI GOOGLE SHEETS =====
    SHEET_ID = "1JG2Vn_qInZrF5OdOIT62L2gu0vqzkP84_WiQFlPDYMo"
    SHEET_NAME = "Rekap Absen"  # nama sheet persis di Google Sheets
    SHEET_NAME_ENCODED = urllib.parse.quote(SHEET_NAME)  # encoding aman untuk spasi
    
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME_ENCODED}"

    # ===== BACA DATA =====
    df = pd.read_csv(url)

    # Bersihkan kolom kosong atau unnamed
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
    df = df.dropna(how="all")

    # Normalisasi nama kolom
    expected_cols = ["Tanggal", "Hari", "Nama", "Jam Masuk", "Jam Pulang"]
    if len(df.columns) >= len(expected_cols):
        df.columns = expected_cols + list(df.columns[len(expected_cols):])

    # Pastikan hanya kolom yang dibutuhkan
    df = df[expected_cols]

    # Konversi tanggal
    df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")
    df = df.dropna(subset=["Tanggal"])

    # Dropdown pegawai
    pegawai_list = ["-- Semua --"] + sorted(df["Nama"].dropna().unique().tolist())
    pegawai = st.selectbox("Pilih Pegawai", pegawai_list)

    if pegawai != "-- Semua --":
        df = df[df["Nama"] == pegawai]

    # ===== TAMPILKAN DATA =====
    st.dataframe(df, use_container_width=True)

    # ===== STATISTIK =====
    if not df.empty:
        hadir = df.groupby("Nama").size().reset_index(name="Jumlah Kehadiran")
        st.subheader("📌 Rekapitulasi Kehadiran")
        st.table(hadir)

        # ===== PLOT ABSENSI =====
        st.subheader("📈 Grafik Kehadiran")

        plt.figure(figsize=(10, 5))
        df_plot = df.groupby("Tanggal").size()
        plt.plot(df_plot.index, df_plot.values, marker="o")
        plt.title("Jumlah Kehadiran per Tanggal")
        plt.xlabel("Tanggal")
        plt.ylabel("Jumlah Pegawai Hadir")
        plt.xticks(rotation=45)
        st.pyplot(plt)

except Exception as e:
    st.error("Gagal membaca file dari Google Sheets!")
    st.code(str(e))
