import streamlit as st
import pandas as pd

st.title("📊 Rekap Absen Pegawai 2025")

# ID Google Sheet kamu
sheet_id = "1Mz_uhB0dVPcwzTxX2M12BQVcc1HVl4U4"
sheet_name = "Rekap Absen"  # sesuai nama tab di Google Sheets
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"

try:
    # Baca data dari Google Sheets
    df = pd.read_csv(url, skiprows=2)  # skip 2 baris karena ada judul di atas tabel

    # Pastikan ada kolom Nama
    if "Nama" not in df.columns:
        st.error("⚠️ Kolom 'Nama' tidak ditemukan di file! Pastikan header di baris ke-3 berisi: Tanggal | Hari | Nama | Jam Masuk | Jam Pulang")
    else:
        st.success("✅ Data berhasil dimuat dari Google Sheets!")

        # Pilihan pegawai
        pegawai = st.selectbox("Pilih Pegawai", ["-- Semua --"] + sorted(df['Nama'].dropna().unique().tolist()))

        # Filter data
        if pegawai != "-- Semua --":
            data_tampil = df[df['Nama'] == pegawai]
        else:
            data_tampil = df

        st.dataframe(data_tampil)

except Exception as e:
    st.error(f"Gagal membaca file dari Google Sheets!\n\n{e}")
