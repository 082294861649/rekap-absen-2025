import streamlit as st
import pandas as pd

st.set_page_config(page_title="📊 Rekap Absen Pegawai 2025", layout="wide")
st.title("📊 Rekap Absen Pegawai 2025")

# Ganti dengan ID file Google Sheet milikmu
sheet_id = "1JG2Vn_qInZrF5OdOIT62L2gu0vqzkP84_WiQFlPDYMo"
# Format URL untuk membaca data CSV dari Google Sheets
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv"

try:
    # File kamu tidak memiliki header di row pertama, jadi header=None
    df = pd.read_csv(url, header=None)

    # Tetapkan nama kolom secara manual sesuai format absen
    df.columns = ["Tanggal", "Hari", "Nama", "Jam Masuk", "Jam Pulang"]

    # Dropdown untuk memilih pegawai
    pegawai = st.selectbox("Pilih Pegawai", ["-- Semua --"] + sorted(df["Nama"].dropna().unique().tolist()))

    # Filter data berdasarkan pegawai pilihan
    if pegawai == "-- Semua --":
        df_tampil = df
    else:
        df_tampil = df[df["Nama"] == pegawai]

    st.subheader("Data Absensi")
    st.dataframe(df_tampil, use_container_width=True)

except Exception as e:
    st.error(f"Gagal membaca file dari Google Sheets!\n\n{e}")
