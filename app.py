import streamlit as st
from fastkml import kml
from shapely.geometry import Point, LineString, Polygon
import pandas as pd

st.title("🗺️ KML to CSV Converter")

uploaded_file = st.file_uploader("Upload KML file nya halah sia boi boi boi", type="kml")

def parse_kml_konten(kml_file):
    doc = kml.KML()
    doc.from_string(kml_file.read())
    features = list(doc.features())

    placemarks = []

    def extract_features(features_list):
        for feature in features_list:
            if hasattr(feature, 'features') and isinstance(feature.features, list) and feature.features:
                extract_features(list(feature.features))  # TANPA tanda kurung setelah 'features'
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

                for lon, lat in coords:  # shapely pakai (x, y) = (lon, lat)
                    placemarks.append({
                        "name": name,
                        "latitude": lat,
                        "longitude": lon
                    })

    extract_features(features)
    return pd.DataFrame(placemarks)


if uploaded_file:
    try:
        df = parse_kml_konten(uploaded_file)
        st.success(f"✅ Berhasil dikonversi! {len(df)} koordinat ditemukan.")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Download CSV", csv, file_name="kml_converted.csv", mime="text/csv")
    except Exception as e:
        st.error(f"Gagal mengonversi file: {e}")
