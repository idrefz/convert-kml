import streamlit as st
from fastkml import kml
from shapely.geometry import Polygon
import pandas as pd

st.set_page_config(page_title="KML Polygon to WKT Converter", layout="centered")
st.title("📐 KML Polygon to WKT Converter")
st.caption("Upload file KML yang berisi Polygon dan akan dikonversi ke format WKT")

uploaded_file = st.file_uploader("Upload KML file", type=["kml"])

if uploaded_file:
    content = uploaded_file.read()

    try:
        doc = kml.KML()
        doc.from_string(content)

        polygons = []

        def extract_polygons(features):
            for feature in features:
                # ambil sub-feature jika ada
                sub_features = getattr(feature, 'features', None)
                if sub_features and not isinstance(sub_features, list):
                    extract_polygons(list(sub_features))
                else:
                    name = getattr(feature, 'name', 'Unnamed')
                    geom = getattr(feature, 'geometry', None)
                    if isinstance(geom, Polygon):
                        polygons.append({
                            "name": name,
                            "wkt": geom.wkt
                        })

        extract_polygons(list(doc.features()))

        if polygons:
            df = pd.DataFrame(polygons)
            st.success("Berhasil mengekstrak Polygon ke WKT!")
            st.dataframe(df)
            st.download_button("⬇️ Download WKT CSV", df.to_csv(index=False), "polygon_wkt.csv", "text/csv")
        else:
            st.warning("Tidak ada polygon ditemukan dalam file KML.")

    except Exception as e:
        st.error(f"Error saat membaca file KML: {e}")
