#!/usr/bin/python
import json
import sys
import subprocess

geojson = sys.argv[1]
dem = sys.argv[2]
geoidHeight = sys.argv[3]

data = json.load(open(geojson));

# https://gis.stackexchange.com/questions/221292/retrieve-pixel-value-with-geographic-coordinate-as-input-with-gdal/221471
def retrieve_pixel_value(geo_coord, data_source):
    """Return floating-point value that corresponds to given point."""
    x, y = geo_coord[0], geo_coord[1]
    forward_transform =  \
        affine.Affine.from_gdal(*data_source.GetGeoTransform())
    reverse_transform = ~forward_transform
    px, py = reverse_transform * (x, y)
    px, py = int(px + 0.5), int(py + 0.5)
    pixel_coord = px, py

    data_array = np.array(data_source.GetRasterBand(1).ReadAsArray())
    return data_array[pixel_coord[0]][pixel_coord[1]] + float(geoidHeight)

def heightcode(arr):
    return float(subprocess.check_output(
        [ "gdallocationinfo", "-valonly" ,"-wgs84", dem, str(arr[0]), str(arr[1]) ])) + float(geoidHeight);

for f in data["features"]:
    if ( f["geometry"]["type"] == "LineString" ):
        for coord in f["geometry"]["coordinates"]:
            coord.append(heightcode(coord));
        print(f["geometry"]["coordinates"])

    elif ( f["geometry"]["type"] == "Point" ):
        coord = f["geometry"]["coordinates"];
        coord.append(heightcode(coord));
        print(f["geometry"]["coordinates"]);

    elif ( f["geometry"]["type"] == "MultiLineString" ):
        for line in f["geometry"]["coordinates"]:
            for coord in line:
                coord.append(heightcode(coord));

with open('heightcoding-out.json', 'w') as fp:
    json.dump(data, fp, indent=4)