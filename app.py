import streamlit as st
import pandas as pd

st.title("📊 Rekap Absen Pegawai 2025")

uploaded_file = st.file_uploader("Unggah file rekap (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Cek apakah ada kolom 'Nama' atau mirip
    possible_cols = [c for c in df.columns if 'nama' in c.lower()]
    if possible_cols:
        col_nama = possible_cols[0]  # ambil kolom pertama yang cocok
    else:
        st.error("Kolom 'Nama' tidak ditemukan di file Excel! Pastikan ada kolom dengan nama 'Nama' atau mirip.")
        st.stop()

    # Dropdown pegawai
    pegawai = st.selectbox(
        "Pilih Pegawai",
        ["-- Semua --"] + sorted(df[col_nama].dropna().unique().tolist())
    )

    # Filter data kalau pegawai dipilih
    if pegawai != "-- Semua --":
        df = df[df[col_nama] == pegawai]

    st.subheader("📑 Data Absen")
    st.dataframe(df)
