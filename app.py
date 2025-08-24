import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Rekap Absen Pegawai 2025", layout="wide")

st.title("📊 Rekap Absen Pegawai 2025")

# ===== KONFIGURASI GOOGLE SHEETS =====
SHEET_ID = "1JG2Vn_qInZrF5OdOIT62L2gu0vqzkP84_WiQFlPDYMo"
SHEET_NAME = "Rekap Absen"

# encode sheet name agar spasi jadi %20
sheet_name_encoded = urllib.parse.quote(SHEET_NAME)
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={sheet_name_encoded}"

# ===== BACA DATA =====
try:
    df = pd.read_csv(url)

    # Bersihkan kolom kosong / unnamed
    df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

    # Tambahkan kolom 'Sumber' dengan nilai dari header jika ada
    if df.columns[0].startswith("Lampiran"):
        sumber = df.columns[0]
        df["Sumber"] = sumber
        df.columns = ["Tanggal", "Hari", "Nama", "Jam Masuk", "Jam Pulang", "Sumber"]
    else:
        # pastikan ada kolom Nama
        expected_cols = ["Tanggal", "Hari", "Nama", "Jam M]()_
