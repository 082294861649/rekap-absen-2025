import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rekap Absen 2025", layout="wide")

st.title("📊 Rekap Absen Pegawai 2025")

# Upload file Excel
uploaded_file = st.file_uploader("Unggah file rekap (Excel)", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file, engine="openpyxl")
    
    st.subheader("Preview Data")
    st.dataframe(df, use_container_width=True)
    
    # Tambah filter nama pegawai
    pegawai = st.selectbox("Pilih Pegawai", ["-- Semua --"] + sorted(df['Nama'].dropna().unique().tolist()))
    
    if pegawai != "-- Semua --":
        df = df[df['Nama'] == pegawai]
    
    st.subheader("Data Terfilter")
    st.dataframe(df, use_container_width=True)
    
    # Rekap per pegawai (contoh hitung jumlah Alpha)
    if 'Keterangan' in df.columns:
        alpha_count = (df['Keterangan'] == "ALPHA").sum()
        st.info(f"Jumlah Alpha: {alpha_count}")
