import streamlit as st
import pandas as pd
import requests
from io import StringIO

def get_weather_icon(condition):
    # Mapping ikon cuaca
    icon_mapping = {
        "cerah": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/cuaca/cerah.png',
        "cerah berawan": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/cuaca/cerah_berawan.png',
        "berawan": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/cuaca/berawan.png',
        "berawan tebal": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/cuaca/berawan_tebal.png',
        "asap": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/cuaca/asap.png',
        "hujan ringan": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/cuaca/hujan_ringan.png',
        "hujan sedang": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/cuaca/hujan_sedang.png',
        "hujan lebat": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/cuaca/hujan_lebat.png',
        "hujan petir": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/cuaca/hujan_petir.png',
        "kabut": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/cuaca/kabut.png'
    }

    icon_path = icon_mapping.get(condition.lower(), 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/error.png')
    return icon_path

def get_winddir_icon(condition):
    # Mapping ikon cuaca
    iconwind_mapping = {
        "utara": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/Utara.png',
        "timur laut": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/Timur_Laut.png',
        "timur": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/Timur.png',
        "tenggara": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/Tenggara.png',
        "selatan": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/Selatan.png',
        "barat daya": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/Barat_Daya.png',
        "barat": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/Barat.png',
        "barat laut": 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/Barat_Laut.png',
    }

    icon2_path = iconwind_mapping.get(condition.lower(), 'https://web.meteo.bmkg.go.id//media/data/bmkg/BIB/winddir/error.png')
    return icon2_path


def show_table_with_icons(data_list, model_name):
    st.write(f"## {model_name} Sites")

    for data in data_list:
        cols = st.columns(8)
        count = 0
        for index, row in data.iterrows():
            with cols[count]:
                st.markdown("""
                    <style>
                    [data-testid=column] [data-testid=stVerticalBlock]{
                        gap: 0.2rem;
                    }
                    </style>
                    """, unsafe_allow_html=True)
                st.write(f"**{row['valid_time']} LT**")
                st.image(get_weather_icon(row["Kondisi_cuaca"]), width=50)
                st.write(row["Kondisi_cuaca"])
                st.write(f"{row['Curah_hujan(mm)']} mm")
                st.write(f"{row['Suhu_udara(C)']} C | {row['Kelembapan_udara(%)']} %")
                st.write(f"Angin")
                st.write(f"{row['Arah_angin']}")
                st.write(f"{row['Kecepatan_angin (km/jam)']} knot")
                st.write(f"Vis {row['Jarak_pandang(m)']} km")
                st.divider()
                count += 1
                if count >= 8:
                    count = 0

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
        data["Kondisi_cuaca"] = data["Kondisi_cuaca"].apply(get_weather_icon)
        data["Arah_angin"] = data["Arah_angin"].apply(get_winddir_icon)
        data_list_a.append(data)

    # Menampilkan tabel dari file CSV script A
    show_table_with_icons(data_list_a, "Model Ina-AROME")


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
        data["Kondisi_cuaca"] = data["Kondisi_cuaca"].apply(get_weather_icon)
        data["Arah_angin"] = data["Arah_angin"].apply(get_winddir_icon)
        data_list_b.append(data)

    # Menampilkan tabel dari file CSV script B
    show_table_with_icons(data_list_b, "Model ECMWF")

def main():
    st.title("INFORMASI PRAKIRAAN CUACA KHUSUS PT. BORNEO INDOBARA")

    # Pilih model menggunakan selectbox
    selected_model = st.selectbox("Pilih Model Cuaca", ["Model Ina-AROME", "Model ECMWF"])

    # Tampilkan konten sesuai model yang dipilih
    if selected_model == "Model Ina-AROME":
        script_a()
    elif selected_model == "Model ECMWF":
        script_b()

if __name__ == "__main__":
    main()