import streamlit as st
import pandas as pd

st.title("📊 Rekap Absen Pegawai 2025")

uploaded_file = st.file_uploader("Unggah file rekap (Excel)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # User pilih kolom mana yang berisi nama pegawai
    col_nama = st.selectbox("Pilih Kolom Nama Pegawai", df.columns)

    pegawai = st.selectbox(
        "Pilih Pegawai",
        ["-- Semua --"] + sorted(df[col_nama].dropna().unique().tolist())
    )

    if pegawai != "-- Semua --":
        df = df[df[col_nama] == pegawai]

    st.subheader("📑 Data Absen")
    st.dataframe(df)
