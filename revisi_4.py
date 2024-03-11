import streamlit as st
import pandas as pd
import requests
from io import StringIO

st.set_page_config(layout="wide")

def get_weather_icon(condition):
    # Mapping ikon cuaca
    icon_mapping = {
        "cerah": f'https://www.bmkg.go.id/asset/img/weather_icon/ID/cerah-am.png',
        "cerah berawan": f'https://www.bmkg.go.id/asset/img/weather_icon/ID/cerah%20berawan-am.png',
        "berawan": f'https://www.bmkg.go.id/asset/img/weather_icon/ID/berawan-am.png',
        "berawan tebal": f'https://www.bmkg.go.id/asset/img/weather_icon/ID/berawan tebal-am.png',
        "asap": f'https://www.bmkg.go.id/asset/img/weather_icon/ID/asap-am.png',
        "hujan ringan": f'https://www.bmkg.go.id/asset/img/weather_icon/ID/hujan%20ringan-am.png',
        "hujan sedang": f'https://www.bmkg.go.id/asset/img/weather_icon/ID/hujan%20sedang-am.png',
        "hujan lebat": f'https://www.bmkg.go.id/asset/img/weather_icon/ID/hujan%20lebat-am.png',
        "hujan petir": f'https://www.bmkg.go.id/asset/img/weather_icon/ID/hujan%20petir-am.png',
        "kabut": f'https://www.bmkg.go.id/asset/img/weather_icon/ID/kabut-am.png'
    }

    icon_path = icon_mapping.get(condition.lower(), f'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/error.png')
    return f'<img src="{icon_path}" style="width: 30px; height: 30px;">'

def get_winddir_icon(condition):
    # Mapping ikon cuaca
    iconwind_mapping = {
        "utara": f'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/Utara.png',
        "timur laut": f'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/Timur_Laut.png',
        "timur": f'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/Timur.png',
        "tenggara": f'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/Tenggara.png',
        "selatan": f'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/Selatan.png',
        "barat daya": f'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/Barat_Daya.png',
        "barat": f'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/Barat.png',
        "barat laut": f'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/Barat_Laut.png',
    }

    icon2_path = iconwind_mapping.get(condition.lower(), f'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/error.png')
    return f'<img src="{icon2_path}" style="width: 30px; height: 30px;">'

# Fungsi untuk menampilkan tabel data dengan ikon
# Fungsi untuk menampilkan tabel data dengan ikon
from datetime import datetime

# ...

# Fungsi untuk menampilkan tabel data dengan ikon
def show_table_with_icons(data, location_name):
    st.subheader(f"Detail Cuaca di Lokasi {location_name}")

    # Mengubah kolom "valid_time" menjadi format datetime
    data['valid_time'] = pd.to_datetime(data['valid_time'])

    # Menambah kolom tanggal dan waktu
    data['Tanggal'] = data['valid_time'].dt.date
    data['Waktu'] = data['valid_time'].dt.time

    # Ganti nilai dalam kolom "Kondisi_cuaca" dengan tag gambar HTML
    data["Kondisi_cuaca"] = data["Kondisi_cuaca"].apply(get_weather_icon)

    # Ganti nilai dalam kolom "Arah_angin" dengan tag gambar HTML
    data["Arah_angin"] = data["Arah_angin"].apply(get_winddir_icon)

    # Reorder kolom sesuai permintaan
    data = data[["Tanggal", "Waktu",
                 "Suhu_udara(C)", "Kelembapan_udara(%)", "Kecepatan_angin (km/jam)",
                 "Arah_angin", "Curah_hujan(mm)", "Kondisi_cuaca", "Jarak_pandang(m)"]]

    # Set kolom "Tanggal" dan "Waktu" sebagai indeks
    data.set_index(["Tanggal", "Waktu"], inplace=True)

    # Konversi DataFrame menjadi HTML
    data_html = data.to_html(escape=False)
    
    # Tambahkan CSS untuk mengatur tata letak tabel dan warna baris
    custom_css = """
        <style>
            table {
                margin-left: auto;
                margin-right: auto;
                text-align: center;
                border-collapse: collapse;
                width: 80%;
            }
            th, td {
                border: 1px solid black;
                padding: 8px;
                text-align: center;  /* Ubah text-align ke center */
            }
            th {
                background-color: #f2f2f2;
            }
            tr:nth-child(even) {
                background-color: #f9f9f9;
            }
            tr:nth-child(odd) {
                background-color: #ffffff;
            }
            th.Tanggal, th.Waktu {
                width: 150px;  /* Menyesuaikan lebar kolom Tanggal dan Waktu */
            }
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # Tampilkan tabel dengan ikon menggunakan IPython.display.HTML
    st.markdown(data_html, unsafe_allow_html=True)


 

def fetch_csv_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error(f"Failed to fetch data from {url}")
        return pd.DataFrame()

def main():
    st.title("INFORMASI PRAKIRAAN CUACA KHUSUS PT. BORNEO INDOBARA")

    # Pilih tab menggunakan selectbox
    selected_location = st.radio("Pilih Lokasi Cuaca", ["AWSKGU", "AWSKGB", "PORTBUNATI", "PASOPATI"])

    # Pilih model menggunakan radio button
    selected_model = st.radio("Pilih Model Cuaca", ["arome", "ecmwf"])

    # Mapping dari nama lokasi ke URL CSV
    location_urls = {
        "Cuaca AWSKGU": {
            "arome": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/fj/AWSKGU_hourly_arome.csv',
            "ecmwf": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/fj/AWSKGU_hourly_ecmwf.csv'
        },
        "Cuaca AWSKGB": {
            "arome": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/fj/AWSKGB_hourly_arome.csv',
            "ecmwf": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/fj/AWSKGB_hourly_ecmwf.csv'
        },
        "Cuaca PORTBUNATI": {
            "arome": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/fj/PORTBUNATI_hourly_arome.csv',
            "ecmwf": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/fj/PORTBUNATI_hourly_ecmwf.csv'
        },
        "Cuaca PASOPATI": {
            "arome": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/fj/PASOPATI_hourly_arome.csv',
            "ecmwf": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/fj/PASOPATI_hourly_ecmwf.csv'
        }
    }

    # Ambil data dari URL yang sesuai dengan lokasi yang dipilih dan modelnya
    selected_data = fetch_csv_data(location_urls[selected_location][selected_model])

    # Tampilkan tabel untuk data yang dipilih
    show_table_with_icons(selected_data, selected_location)

if __name__ == "__main__":
    main()
