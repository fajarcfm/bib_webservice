import streamlit as st
import pandas as pd
import requests
from io import StringIO

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



# Fungsi untuk menampilkan peta dengan marker lokasi dari data CSV
#def show_map(data_list):
#    all_data = pd.concat(data_list)
#    st.map(all_data)

# Fungsi untuk menampilkan tabel data dengan ikon
def show_table_with_icons(data_list):
    for idx, data in enumerate(data_list, 1):
        st.subheader(f"Cuaca Lokasi {idx}: {data['Lokasi'].iloc[0]} Longitude {data['lon'].iloc[0]} Latitude {data['lat'].iloc[0]}")
        
        # Ganti nilai dalam kolom "Kondisi_cuaca" dengan tag gambar HTML
        data["Kondisi_cuaca"] = data["Kondisi_cuaca"].apply(get_weather_icon)

        # Ganti nilai dalam kolom "Kondisi_cuaca" dengan tag gambar HTML
        data["Arah_angin"] = data["Arah_angin"].apply(get_winddir_icon)

        # Reorder kolom sesuai permintaan
        data = data[["valid_time", 
                     "Suhu_udara(C)", "Kelembapan_udara(%)", "Kecepatan_angin (km/jam)", 
                     "Arah_angin", "Curah_hujan(mm)", "Kondisi_cuaca", "Jarak_pandang(m)"]]

        # Set kolom "valid_time" sebagai indeks
        data.set_index("valid_time", inplace=True)

        # Transpose DataFrame untuk mendapatkan tampilan yang diinginkan
        data_transposed = data.T

        # Konversi DataFrame menjadi HTML
        data_html = data_transposed.to_html(escape=False)

        # Tampilkan tabel dengan ikon 
        st.markdown(data_html, unsafe_allow_html=True)


def fetch_csv_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(StringIO(response.text))
    else:
        st.error(f"Failed to fetch data from {url}")
        return pd.DataFrame()

def script_a():
    st.title("Model Ina-Arome")

    # Specify the URLs for script A
    csv_urls_a = [
        'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/fj/AWSKGU_hourly_arome.csv',
        'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/fj/AWSKGB_hourly_arome.csv',
        'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/fj/PORTBUNATI_hourly_arome.csv',
        'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/fj/PASOPATI_hourly_arome.csv'
    ]

    data_list_a = []

    for csv_url in csv_urls_a:
        # Fetch data from URL
        data = fetch_csv_data(csv_url)
        data_list_a.append(data)

    # Menampilkan tabel dari file CSV script A
    show_table_with_icons(data_list_a)

    # Menampilkan peta dengan semua titik dari file CSV script A
#    st.subheader("Peta Lokasi Model AROME:")
#    show_map(data_list_a)

def script_b():
    st.title("Model ECMWF")

    # Specify the URLs for script B
    csv_urls_b = [
        'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/fj/AWSKGU_hourly_ecmwf.csv',
        'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/fj/AWSKGB_hourly_ecmwf.csv',
        'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/fj/PORTBUNATI_hourly_ecmwf.csv',
        'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/fj/PASOPATI_hourly_ecmwf.csv'
    ]

    data_list_b = []

    for csv_url in csv_urls_b:
        # Fetch data from URL
        data = fetch_csv_data(csv_url)
        data_list_b.append(data)

    # Menampilkan tabel dari file CSV script B
    show_table_with_icons(data_list_b)

    # Menampilkan peta dengan semua titik dari file CSV script B
 #   st.subheader("Peta Lokasi Model ECMWF:")
 #   show_map(data_list_b)

def main():
    st.title("INFORMASI PRAKIRAAN CUACA KHUSUS PT. BORNEO INDOBARA")

    # Pilih tab menggunakan selectbox
    selected_tab = st.radio("Pilih Model Cuaca", ["Model Ina-AROME", "Model ECMWF"])

    # Tampilkan konten sesuai tab yang dipilih
    if selected_tab == "Model Ina-AROME":
        script_a()
    elif selected_tab == "Model ECMWF":
        script_b()

if __name__ == "__main__":
    main()
