import streamlit as st
from fastkml import kml
from shapely.geometry import Point, LineString, Polygon
import pandas as pd

st.set_page_config(page_title="KML to CSV Converter", layout="centered")
st.title("🗺️ KML to CSV Converter")
st.caption("Upload KML file nya halah sia boi boi boi")

uploaded_file = st.file_uploader("Upload KML file", type=["kml"])

if uploaded_file is not None:
    try:
        content = uploaded_file.read()

        doc = kml.KML()
        doc.from_string(content)

        placemarks = []

        def extract_features(features):
            for feature in features:
                if hasattr(feature, 'features') and callable(getattr(feature, 'features', None)):
                    extract_features(list(feature.features()))
                else:
                    name = getattr(feature, 'name', '')
                    geom = getattr(feature, 'geometry', None)
                    if geom is None:
                        continue

                    if isinstance(geom, Point):
                        coords = [(geom.y, geom.x)]
                    elif isinstance(geom, LineString):
                        coords = list(geom.coords)
                    elif isinstance(geom, Polygon):
                        coords = list(geom.exterior.coords)
                    else:
                        coords = []

                    for lon, lat in coords:
                        placemarks.append({
                            "name": name,
                            "latitude": lat,
                            "longitude": lon
                        })

        extract_features(list(doc.features()))

        if placemarks:
            df = pd.DataFrame(placemarks)
            st.success("Berhasil mengonversi file! Silakan download hasilnya.")
            st.dataframe(df)
            st.download_button("⬇️ Download CSV", df.to_csv(index=False), "converted_kml.csv", "text/csv")
        else:
            st.warning("Tidak ada koordinat yang ditemukan dalam file KML.")

    except Exception as e:
        st.error(f"Gagal mengonversi file: {e}")
