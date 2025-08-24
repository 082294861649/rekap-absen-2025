import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="📊 Rekap Absen Pegawai 2025", layout="wide")

st.title("📊 Rekap Absen Pegawai 2025")

# --- Link Google Sheet ---
SHEET_ID = "1JG2Vn_qInZrF5OdOIT62L2gu0vqzkP84_WiQFlPDYMo"
SHEET_NAME = "Rekap_Absen"
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

try:
    df = pd.read_csv(url)

    # --- Pembersihan kolom ---
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.columns = [c.strip() for c in df.columns]

    expected_cols = ["Tanggal", "Hari", "Nama", "Jam Masuk", "Jam Pulang"]
    df = df.iloc[:, :len(expected_cols)]
    df.columns = expected_cols

    # --- Konversi Tanggal ---
    df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")

    # --- Daftar libur nasional (contoh, bisa ditambah sesuai kalender resmi) ---
    libur_nasional = [
        "2025-01-01",  # Tahun Baru
        "2025-03-31",  # Nyepi
        "2025-04-18",  # Wafat Isa
        "2025-05-01",  # Hari Buruh
        "2025-05-29",  # Kenaikan Isa
        "2025-06-01",  # Hari Lahir Pancasila
        "2025-06-06",  # Idul Adha (contoh)
    ]

    def is_libur(tanggal, hari):
        tanggal_str = str(tanggal.date())
        if hari == "Minggu":
            return True
        if tanggal_str in libur_nasional:
            return True
        return False

    # --- Pilihan Pegawai ---
    pegawai = st.selectbox("Pilih Pegawai", ["-- Semua --"] + sorted(df["Nama"].dropna().unique().tolist()))

    if pegawai != "-- Semua --":
        data = df[df["Nama"] == pegawai]
    else:
        data = df.copy()

    st.dataframe(data)

    # --- Plot Kehadiran ---
    colors = ["red" if is_libur(t, h) else "blue" for t, h in zip(data["Tanggal"], data["Hari"])]

    plt.figure(figsize=(12, 4))
    plt.scatter(data["Tanggal"], [1]*len(data), c=colors)
    plt.yticks([])
    plt.title(f"Kehadiran {'Semua Pegawai' if pegawai=='-- Semua --' else pegawai}")
    st.pyplot(plt)

except Exception as e:
    st.error(f"Gagal membaca file dari Google Sheets!\n\n{e}")
