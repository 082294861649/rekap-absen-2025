import streamlit as st
import pandas as pd

st.title("📊 Rekap Absen Pegawai 2025")

# ID Google Sheets kamu
sheet_id = "1Mz_uhB0dVPcwzTxX2M12BQVcc1HVl4U4"
sheet_name = "Rekap%20Absen"  # encode spasi pakai %20

url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

try:
    df = pd.read_csv(url)

    # Pastikan kolom yang dibaca sesuai
    if "Nama" not in df.columns:
        st.error("⚠️ Kolom 'Nama' tidak ditemukan di file! Periksa kembali header Google Sheets.")
    else:
        # Pilih pegawai
        pegawai = st.selectbox("Pilih Pegawai", ["-- Semua --"] + sorted(df['Nama'].dropna().unique().tolist()))

        if pegawai != "-- Semua --":
            data = df[df['Nama'] == pegawai]
        else:
            data = df

        st.dataframe(data)

except Exception as e:
    st.error(f"Gagal membaca file dari Google Sheets!\n\n{e}")
