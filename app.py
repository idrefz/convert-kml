import streamlit as st
import geopandas as gpd
import pandas as pd
import io
from shapely.geometry import Point

st.set_page_config(page_title="Proyek ke STO Mapper", layout="wide")
st.title("🔗 Mapping Proyek ke Polygon STO (Spatial Join)")

# 1. Upload file polygon STO (KML)
st.header("1. Upload KML STO (Polygon Wilayah)")
kml_file = st.file_uploader("Upload file KML (Polygon STO)", type=["kml"])

# 2. Upload proyek dengan koordinat
st.header("2. Upload File Proyek (dengan Koordinat)")
proyek_file = st.file_uploader("Upload file Excel/CSV proyek", type=["xlsx", "csv"])

# 3. Proses jika kedua file sudah diupload
if kml_file and proyek_file:
    try:
        # Read KML ke GeoDataFrame
        gdf_sto = gpd.read_file(kml_file, driver='KML')

        # Read proyek file
        if proyek_file.name.endswith(".csv"):
            df_proyek = pd.read_csv(proyek_file)
        else:
            df_proyek = pd.read_excel(proyek_file)

        # Validasi kolom koordinat
        if not {'latitude', 'longitude'}.issubset(df_proyek.columns):
            st.error("File proyek harus memiliki kolom 'latitude' dan 'longitude'")
        else:
            # Convert proyek ke GeoDataFrame
            geometry = [Point(xy) for xy in zip(df_proyek['longitude'], df_proyek['latitude'])]
            gdf_proyek = gpd.GeoDataFrame(df_proyek, geometry=geometry, crs="EPSG:4326")

            # Pastikan STO GeoDataFrame juga pakai EPSG:4326
            gdf_sto = gdf_sto.to_crs("EPSG:4326")

            # Spatial Join
            hasil = gpd.sjoin(gdf_proyek, gdf_sto, how="left", predicate='within')

            # Tampilkan hasil
            st.header("3. Hasil Mapping Proyek ke STO")
            st.dataframe(hasil)

            # Download hasil
            st.download_button(
                label="📥 Download Hasil ke Excel",
                data=hasil.drop(columns='geometry').to_excel(index=False, engine='openpyxl'),
                file_name="hasil_mapping_proyek.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # Tampilkan di peta
            st.header("4. Visualisasi di Peta")
            st.map(gdf_proyek)

    except Exception as e:
        st.error(f"Terjadi error: {str(e)}")
