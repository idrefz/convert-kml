import streamlit as st
from fastkml import kml
from shapely.geometry import Point, LineString, Polygon
import pandas as pd
import io

st.set_page_config(page_title="KML to Excel Converter", layout="centered")

st.title("📍 KML to Excel Converter")
st.markdown("Upload file `.kml` dan konversi ke `.xlsx` (Excel).")

uploaded_file = st.file_uploader("Unggah file KML", type="kml")

if uploaded_file is not None:
    try:
        doc = kml.KML()
        doc.from_string(uploaded_file.read())

        placemarks = []

        def extract_features(features_list):
            for feature in features_list:
                if hasattr(feature, 'features') and isinstance(feature.features, list) and feature.features:
                    extract_features(feature.features)
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

        df = pd.DataFrame(placemarks)

        if not df.empty:
            st.success(f"Berhasil mengonversi {len(df)} data koordinat.")
            st.dataframe(df)

            # Simpan ke file Excel di memori
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name="KML Data")
            st.download_button(
                label="📥 Download Excel",
                data=output.getvalue(),
                file_name="converted_kml.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Tidak ada data koordinat ditemukan dalam file KML.")

    except Exception as e:
        st.error(f"Gagal mengonversi file: {e}")
