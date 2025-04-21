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
                if hasattr(feature, 'features') and callable(getattr(feature, 'features', None)):
                    extract_polygons(list(feature.features()))
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
            st.success("Berhasil mengekstrak WKT dari Polygon!")
            st.dataframe(df)
            st.download_button("⬇️ Download WKT CSV", df.to_csv(index=False), "polygon_wkt.csv", "text/csv")
        else:
            st.warning("Tidak ditemukan polygon di file KML.")

    except Exception as e:
        st.error(f"Error saat membaca file KML: {e}")
