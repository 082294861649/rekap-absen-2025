import streamlit as st
import pandas as pd

st.set_page_config(page_title="📊 Rekap Absen Pegawai 2025", layout="wide")

st.title("📊 Rekap Absen Pegawai 2025")

# ID Google Sheet (ganti sesuai file kamu)
sheet_id = "1JDe9Ldrk8IMJZjzhUVDXBA5B-ZptkoI1"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"

# Baca data dari Google Sheets
try:
    df = pd.read_csv(url)

    # Pastikan kolom Nama ada
    if "Nama" not in df.columns:
        st.error("⚠️ Kolom 'Nama' tidak ditemukan di file! Periksa kembali Google Sheets.")
    else:
        # Pilihan pegawai
        pegawai = st.selectbox(
            "Pilih Pegawai",
            ["-- Semua --"] + sorted(df["Nama"].dropna().unique().tolist())
        )

        # Filter data
        if pegawai != "-- Semua --":
            data_filtered = df[df["Nama"] == pegawai]
        else:
            data_filtered = df

        # Tampilkan data
        st.dataframe(data_filtered, use_container_width=True)

        # Rekap kehadiran
        if "Status" in df.columns:
            st.subheader("📌 Rekap Kehadiran")
            rekap = data_filtered["Status"].value_counts()
            st.bar_chart(rekap)

except Exception as e:
    st.error(f"❌ Gagal membaca data dari Google Sheets.\n\nError: {e}")
