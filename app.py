import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import urllib.parse
from datetime import datetime

st.set_page_config(page_title='📊 Rekap Absen Pegawai 2025', layout='wide')
st.title('📊 Rekap Absen Pegawai 2025')

# =========================
# KONFIGURASI GOOGLE SHEETS
# =========================
SHEET_ID = '1JG2Vn_qInZrF5OdOIT62L2gu0vqzkP84_WiQFlPDYMo'
SHEET_NAME = 'Rekap Absen'  # pastikan sesuai
SHEET_NAME_ENCODED = urllib.parse.quote(SHEET_NAME)  # encode spasi & karakter khusus
CSV_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME_ENCODED}'

# =========================
# DAFTAR LIBUR NASIONAL 2025
# (sesuaikan jika ada perubahan)
# =========================
LIBUR_NASIONAL_STR = [
    '2025-01-01',  # Tahun Baru
    '2025-01-29',  # Imlek (perkiraan)
    '2025-03-31',  # Nyepi (perkiraan)
    '2025-04-18',  # Wafat Isa Almasih
    '2025-05-01',  # Hari Buruh
    '2025-05-29',  # Kenaikan Isa Almasih
    '2025-06-01',  # Hari Lahir Pancasila
    '2025-08-17',  # HUT RI
    '2025-08-18',  # Pengganti HUT RI (sesuai konteks pengguna)
]
LIBUR_NASIONAL = pd.to_datetime(LIBUR_NASIONAL_STR, errors='coerce').date

HARI_ID = ['Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Minggu']

def hari_id(dt: pd.Timestamp) -> str:
    if pd.isna(dt):
        return ''
    return HARI_ID[dt.weekday()]

def build_dataframe_from_csv(url: str) -> pd.DataFrame:
    # Baca CSV dengan robust fallback
    df = pd.read_csv(url, header=None, dtype=str)
    if df.shape[1] == 1:
        # fallback jika delimiter bukan koma
        try:
            alt = pd.read_csv(url, header=None, dtype=str, sep=';')
            if alt.shape[1] > 1:
                df = alt
        except Exception:
            pass

    # Buang kolom & baris kosong
    df = df.dropna(how='all')
    df = df.dropna(axis=1, how='all')

    # Buang baris "Lampiran ..." jika ada di baris teratas
    if not df.empty:
        first_row_str = ' '.join([str(x) for x in df.iloc[0].tolist()]).lower()
        if 'lampiran' in first_row_str:
            df = df.iloc[1:].reset_index(drop=True)

    # Pastikan minimal 5 kolom dengan padding
    expected_cols = ['Tanggal','Hari','Nama','Jam Masuk','Jam Pulang']
    col_count = df.shape[1]
    data = {}
    for i, col_name in enumerate(expected_cols):
        if i < col_count:
            data[col_name] = df.iloc[:, i]
        else:
            data[col_name] = pd.Series([None]*len(df), index=df.index)

    out = pd.DataFrame(data)

    # Konversi tanggal
    out['Tanggal'] = pd.to_datetime(out['Tanggal'], errors='coerce')

    # Isi Hari jika kosong
    mask_hari_kosong = out['Hari'].isna() | (out['Hari'].astype(str).str.strip() == '')
    out.loc[mask_hari_kosong, 'Hari'] = out.loc[mask_hari_kosong, 'Tanggal'].apply(hari_id)

    # Rapikan whitespace
    for c in ['Hari','Nama','Jam Masuk','Jam Pulang']:
        out[c] = out[c].astype(str).str.strip()

    # Buang baris tanpa tanggal valid
    out = out.dropna(subset=['Tanggal']).reset_index(drop=True)

    return out

try:
    df = build_dataframe_from_csv(CSV_URL)

    # Tambahkan kolom bulan (nama Indonesia)
    BULAN_ID = {
        1:'Januari',2:'Februari',3:'Maret',4:'April',5:'Mei',6:'Juni',
        7:'Juli',8:'Agustus',9:'September',10:'Oktober',11:'November',12:'Desember'
    }
    df['Bulan'] = df['Tanggal'].dt.month.map(BULAN_ID)

    # Flag libur: Minggu ATAU masuk daftar libur nasional
    df['Tanggal_date'] = df['Tanggal'].dt.date
    df['Libur'] = (df['Hari'].eq('Minggu')) | (df['Tanggal_date'].isin(LIBUR_NASIONAL))

    # ======= FILTER =======
    col1, col2 = st.columns(2)
    with col1:
        bulan_opt = ['-- Semua --'] + sorted(df['Bulan'].dropna().unique().tolist(),
                                             key=lambda x: list(BULAN_ID.values()).index(x))
        bulan = st.selectbox('Filter Bulan', bulan_opt)
    with col2:
        pegawai_opt = ['-- Semua --'] + sorted(df['Nama'].dropna().unique().tolist())
        pegawai = st.selectbox('Filter Pegawai', pegawai_opt)

    df_filtered = df.copy()
    if bulan != '-- Semua --':
        df_filtered = df_filtered[df_filtered['Bulan'] == bulan]
    if pegawai != '-- Semua --':
        df_filtered = df_filtered[df_filtered['Nama'] == pegawai]

    # ======= TABEL DENGAN HIGHLIGHT LIBUR =======
    def style_libur(row):
        if bool(row['Libur']):
            return ['background-color: #ffd6d6'] * len(row)  # merah muda
        return [''] * len(row)

    st.subheader('📅 Data Kehadiran')
    try:
        st.dataframe(df_filtered.style.apply(style_libur, axis=1), use_container_width=True)
    except Exception:
        # fallback jika styler bermasalah
        st.dataframe(df_filtered, use_container_width=True)

    # ======= REKAP & GRAFIK =======
    st.subheader('📈 Rekap Kehadiran')
    rekap = df_filtered.groupby('Nama').size().reset_index(name='Jumlah Hadir')
    if not rekap.empty:
        st.dataframe(rekap, use_container_width=True)

        # Grafik jumlah hadir per bulan
        st.subheader('📊 Grafik Jumlah Hadir per Bulan')
        per_bulan = df_filtered.groupby(['Bulan']).size().reindex(list(BULAN_ID.values()), fill_value=0)
        fig, ax = plt.subplots(figsize=(8,4))
        ax.bar(per_bulan.index, per_bulan.values)
        ax.set_xlabel('Bulan')
        ax.set_ylabel('Jumlah Hadir')
        ax.set_title('Jumlah Hadir per Bulan')
        plt.xticks(rotation=30, ha='right')
        st.pyplot(fig)
    else:
        st.info('Tidak ada data untuk filter yang dipilih.')

except Exception as e:
    st.error('Gagal membaca file dari Google Sheets!')
    st.code(str(e))
