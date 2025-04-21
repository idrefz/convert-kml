from fastkml import kml
from shapely.geometry import Point, LineString, Polygon
import pandas as pd

# Ubah path di bawah sesuai lokasi file KML kamu
kml_file_path = "sto.kml"
output_file_path = "sto_output.xlsx"

with open(kml_file_path, 'rb') as f:
    content = f.read()

doc = kml.KML()
doc.from_string(content)

placemarks = []

def extract_features(features):
    for feature in features:
        if hasattr(feature, 'features') and callable(feature.features):
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

df = pd.DataFrame(placemarks)
df.to_excel(output_file_path, index=False)

print(f"Berhasil disimpan ke {output_file_path}")
