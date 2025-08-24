import streamlit as st
import pandas as pd

st.set_page_config(page_title="📊 Rekap Absen Pegawai 2025", layout="wide")

st.title("📊 Rekap Absen Pegawai 2025")

# --- LINK GOOGLE SHEETS ---
SHEET_ID = "1JG2Vn_qInZrF5OdOIT62L2gu0vqzkP84_WiQFlPDYMo"
SHEET_NAME = "Rekap Absen"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

# --- DAFTAR LIBUR NASIONAL 2025 (contoh, bisa ditambah manual) ---
libur_nasional = [
    "2025-01-01",  # Tahun Baru
    "2025-03-31",  # Nyepi
    "2025-04-18",  # Wafat Isa
    "2025-05-01",  # Hari Buruh
    "2025-05-29",  # Kenaikan Isa
    "2025-06-01",  # Hari Pancasila
    "2025-08-17",  # Kemerdekaan
]
libur_nasional = pd.to_datetime(libur_nasional)

try:
    df = pd.read_csv(url)

    # 🔹 Bersihkan baris kosong & header tambahan
    df = df.dropna(how="all")
    df = df[df.columns[:5]]
    df.columns = ["Tanggal", "Hari", "Nama", "Jam Masuk", "Jam Pulang"]

    # 🔹 Konversi tanggal
    df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")

    # 🔹 Tambahkan kolom Bulan
    df["Bulan"] = df["Tanggal"].dt.strftime("%B")

    # --- FILTER ---
    bulan = st.selectbox("Pilih Bulan", ["-- Semua --"] + sorted(df["Bulan"].dropna().unique().tolist()))
    pegawai = st.selectbox("Pilih Pegawai", ["-- Semua --"] + sorted(df["Nama"].dropna().unique().tolist()))

    df_filtered = df.copy()
    if bulan != "-- Semua --":
        df_filtered = df_filtered[df_filtered["Bulan"] == bulan]
    if pegawai != "-- Semua --":
        df_filtered = df_filtered[df_filtered["Nama"] == pegawai]

    # --- HIGHLIGHT MINGGU & LIBUR ---
    def highlight_libur(row):
        if pd.isna(row["Tanggal"]):
            return [""] * len(row)
        if row["Hari"] == "Minggu" or row["Tanggal"] in libur_nasional:
            return ["background-color: #ffcccc"] * len(row)  # merah muda
        return [""] * len(row)

    st.subheader("📅 Data Kehadiran")
    st.dataframe(
        df_filtered.style.apply(highlight_libur, axis=1),
        use_container_width=True
    )

    # --- GRAFIK JUMLAH ABSEN ---
    st.subheader("📈 Statistik Kehadiran")
    hadir = df.groupby("Nama").size().reset_index(name="Ju_
