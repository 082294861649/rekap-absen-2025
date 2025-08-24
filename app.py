import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import calendar
from datetime import datetime

st.set_page_config(page_title="📊 Rekap Absen Pegawai 2025", layout="wide")

st.title("📊 Rekap Absen Pegawai 2025")

# =======================
# Konfigurasi Google Sheet
# =======================
SHEET_ID = "1JG2Vn_qInZrF5OdOIT62L2gu0vqzkP84_WiQFlPDYMo"
SHEET_NAME = "Rekap Absen"   # pastikan sesuai dengan nama sheet
url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"

# =======================
# Load Data
# =======================
try:
    df = pd.read_csv(url)

    # Bersihkan kolom tanpa nama
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.columns = [c.strip() for c in df.columns]

    # Standarisasi jumlah kolom
    expected_cols = ["Tanggal", "Hari", "Nama", "Jam Masuk", "Jam Pulang"]
    df = df.iloc[:, :len(expected_cols)]
    while df.shape[1] < len(expected_cols):
        df[f"Extra_{df.shape[1]}"] = ""
    df = df.iloc[:, :len(expected_cols)]
    df.columns = expected_cols

    # Format tanggal
    df["Tanggal"] = pd.to_datetime(df["Tanggal"], errors="coerce")

    # Buang baris tanpa nama
    df = df.dropna(subset=["Nama"])

except Exception as e:
    st.error(f"Gagal membaca file dari Google Sheets!\n\n{e}")
    st.stop()

# =======================
# Input User
# =======================
pegawai = st.selectbox("👤 Pilih Pegawai", ["-- Semua --"] + sorted(df["Nama"].dropna().unique().tolist()))
tahun = st.selectbox("📅 Pilih Tahun", sorted(df["Tanggal"].dt.year.dropna().unique().tolist()))

# =======================
# Filter Data
# =======================
df_tahun = df[df["Tanggal"].dt.year == tahun]
if pegawai != "-- Semua --":
    df_tahun = df_tahun[df_tahun["Nama"] == pegawai]

st.subheader("📑 Data Absensi")
st.dataframe(df_tahun)

# =======================
# Kalender Absensi
# =======================
st.subheader("🗓️ Kalender Absensi")

# Daftar libur nasional (contoh, bisa ditambahkan manual)
libur_nasional = [
    "2025-01-01",  # Tahun Baru
    "2025-03-31",  # Nyepi
    "2025-04-18",  # Wafat Isa Almasih
    "2025-05-01",  # Hari Buruh
    "2025-05-29",  # Kenaikan Isa Almasih
    "2025-06-01",  # Hari Lahir Pancasila
    "2025-08-17",  # HUT RI
]
libur_nasional = pd.to_datetime(libur_nasional, errors="coerce")

bulan = st.selectbox("📆 Pilih Bulan", list(calendar.month_name)[1:])
bulan_idx = list(calendar.month_name).index(bulan)

df_bulan = df_tahun[df_tahun["Tanggal"].dt.month == bulan_idx]

# Buat kalender
cal = calendar.Calendar(firstweekday=0)
hari = ["Sen", "Sel", "Rab", "Kam", "Jum", "Sab", "Min"]

fig, ax = plt.subplots(figsize=(10, 6))
ax.set_axis_off()
ax.set_title(f"Kalender {bulan} {tahun}", fontsize=16, weight="bold")

# Header hari
for i, h in enumerate(hari):
    ax.text(i, 0, h, ha="center", va="center", fontsize=12, weight="bold")

# Isi tanggal
row = 1
for week in cal.monthdatescalendar(tahun, bulan_idx):
    for i, day in enumerate(week):
        if day.month != bulan_idx:
            continue

        color = "black"
        bgcolor = "white"

        # Cek Minggu → merah
        if day.weekday() == 6:
            color = "red"
        # Cek Sabtu → biru (kecuali libur nasional → merah)
        elif day.weekday() == 5:
            if day in libur_nasional.values:
                color = "red"
            else:
                color = "blue"

        # Cek hadir
        if pegawai != "-- Semua --":
            if day in df_bulan["Tanggal"].values:
                if day in df_bulan[df_bulan["Nama"] == pegawai]["Tanggal"].values:
                    bgcolor = "#90EE90"  # hijau jika hadir

        ax.add_patch(plt.Rectangle((i-0.5, row-0.5), 1, 1, fill=True, color=bgcolor, alpha=0.3))
        ax.text(i, row, str(day.day), ha="center", va="center", fontsize=12, color=color)

    row += 1

st.pyplot(fig)
