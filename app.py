import streamlit as st
import pandas as pd

st.set_page_config(page_title="📊 Rekap Absen Pegawai 2025", layout="wide")

st.title("📊 Rekap Absen Pegawai 2025")

# === Load data dari Google Sheets ===
sheet_id = "1Mz_uhBOdVPcwzTxX2M12BQVcC1HVl4U4"  # ganti dengan sheet ID kamu
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

try:
    # skiprows=1 karena baris pertama hanya judul
    df = pd.read_csv(url, skiprows=1)

    # Pastikan kolom Nama ada
    if "Nama" not in df.columns:
        st.error("⚠️ Kolom 'Nama' tidak ditemukan di file! Periksa header file Excel/Sheets.")
        st.write("Kolom yang terbaca:", df.columns.tolist())
    else:
        # Dropdown pilih pegawai
        pegawai = st.selectbox("Pilih Pegawai", ["-- Semua --"] + sorted(df['Nama'].dropna().unique().tolist()))

        # Filter data
        if pegawai != "-- Semua --":
            df_filtered = df[df['Nama'] == pegawai]
        else:
            df_filtered = df

        st.subheader("📋 Data Absensi")
        st.dataframe(df_filtered, use_container_width=True)

        # Rekap sederhana
        st.subheader("📈 Rekap Kehadiran")
        rekap = df_filtered.groupby("Nama").size().reset_index(name="Jumlah Kehadiran")
        st.dataframe(rekap, use_container_width=True)

except Exception as e:
    st.error("Gagal membaca file dari Google Sheets!")
    st.exception(e)
