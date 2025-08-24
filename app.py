import streamlit as st
import pandas as pd

st.set_page_config(page_title="Rekap Absen Pegawai 2025", layout="wide")

st.title("📊 Rekap Absen Pegawai 2025")

# URL Google Sheets CSV (ganti ID dan sheet sesuai milikmu)
SHEET_ID = "1JG2Vn_qInZrF5OdOIT62L2gu0vqzkP84_WiQFlPDYMo"
SHEET_NAME = "Rekap Absen"  # nama sheet persis dari Google Sheets
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

try:
    # baca data
    df = pd.read_csv(url, header=None)

    # buang kolom kosong jika ada
    df = df.dropna(axis=1, how="all")

    # set header kolom sesuai format absensi
    df.columns = ["Tanggal", "Hari", "Nama", "Jam Masuk", "Jam Pulang"]

    # filter pegawai
    pegawai_list = ["-- Semua --"] + sorted(df["Nama"].dropna().unique().tolist())
    pegawai = st.selectbox("Pilih Pegawai", pegawai_list)

    if pegawai != "-- Semua --":
        df = df[df["Nama"] == pegawai]

    # tampilkan tabel
    st.dataframe(df, use_container_width=True)

    # unduh CSV
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Unduh Rekap CSV",
        data=csv,
        file_name="rekap_absen.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error(f"Gagal membaca file dari Google Sheets!\n\n{e}")
