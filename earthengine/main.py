import ee
import numpy as np
import geopy
from geopy import distance
from io import StringIO


service_account = "local-host@ee-tornado-tracks.iam.gserviceaccount.com"
credentials = ee.ServiceAccountCredentials(service_account, r"/Users/nolan/Downloads/download temp/ee-tornado-tracks-94b11e113970.json")
ee.Initialize(credentials)

def get_center(lat1, lon1, lat2, lon2):
    """
    Returns the centerpoint (lat, lon) of a line drawn between two given coordinate pairs
    """
    center_lat = (lat1 + lat2) / 2
    center_lon = (lon1 + lon2) / 2
    return (center_lat, center_lon)

def bbox_from_point(bbox_size, lat_point, lon_point):
    """
    bbox_size - either square in km (one value) or two values in NS km (height), then EW km (width)
    lat_point - lat center of bounding box
    lon_point - lon center of bounding box

    returns ee.Geometry object of bounding box
    """
    if type(bbox_size) == int or type(bbox_size) == float:
        bbox_size = np.array([bbox_size])

    if len(bbox_size) == 1:
        lat_km = bbox_size[0]
        lon_km = bbox_size[0]
    elif len(bbox_size) == 2:
        lat_km, lon_km = bbox_size
    else:
        raise ValueError("bbox_size must be either length 1 or 2")

    origin = geopy.Point(lat_point, lon_point)
    lat_min = (
        distance.geodesic(kilometers=lat_km / 2).destination(origin, bearing=180)
    )[0]
    lat_max = (
        distance.geodesic(kilometers=lat_km / 2).destination(origin, bearing=0)
    )[0]
    lon_min = (
        distance.geodesic(kilometers=lon_km / 2).destination(origin, bearing=270)
    )[1]
    lon_max = (
        distance.geodesic(kilometers=lon_km / 2).destination(origin, bearing=90)
    )[1]

    return ee.Geometry.BBox(lon_min, lat_min, lon_max, lat_max)

def get_ew_km(lat1, lon1, lon2):
    """
    Given the longitude of two points(a, b), and the latitude of a point(a), returns the 
    EAST --> WEST km distance from point(a) to point(b)
    """
    point_a = (lat1, lon1)
    point_b = (lat1, lon2)
    dist = distance.geodesic(point_a, point_b).kilometers
    return dist

def get_ns_km(lat1, lon1, lat2):
    """
    Given the latitude of two points(a, b), and the longitude of a point(a), returns the 
    NORTH --> SOUTH km distance from point(a) to point(b)
    """
    point_a = (lat1, lon1)
    point_b = (lat2, lon1)
    dist = distance.geodesic(point_a, point_b).kilometers
    return dist

def image_dimensions(lat_length, lon_length):
    """
    Given a height (lat) and width (lon) in km, returns proper dimensions of a 10M or better image for use in ee.Image retrieval 
    * might cause problems if tornado is too long, and should be tweaked in the future to be more browser friendly
    """
    if lat_length >= lon_length:
        # max_dim = length
        x_dim = int(lat_length * 100)
        ratio = lon_length / lat_length
        y_dim = int(x_dim * ratio)
        return x_dim, y_dim
    else:
        y_dim = int(lon_length * 100)
        ratio = lat_length / lon_length
        x_dim = int(y_dim * ratio)
        return y_dim, x_dim

def main():
    center = get_center(35.284,-97.628,35.341,-97.3999)
    print(center)
    ns = get_ns_km(35.284, -97.628, 35.341)
    ew = get_ew_km(35.284, -97.628, -97.3999)
    size = (ns, ew)
    bbox = bbox_from_point(size, center[0], center[1])

    # compact way of storing an ee image collection ?
    moore_before_collection = (
    ee.ImageCollection("COPERNICUS/S2_HARMONIZED")
    .filterBounds(bbox)
    .filterDate("1980-05-20", "2021-05-20")
    .filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", 10))
    )

    moore_before_image = ee.Image(moore_before_collection.first())

    x_dim, y_dim = image_dimensions(ns, ew)
    print(str(x_dim))
    print(str(y_dim))

    # getThumbURL ?
    moore_before_url = moore_before_image.getThumbURL(
    {
        "format": "png",
        "bands": ["B4", "B3", "B2"],
        "dimensions": [x_dim, y_dim],
        "region": bbox,
        "min": 0,
        "max": 4000,
    }
    )   

    moore_after_collection = (
    ee.ImageCollection("COPERNICUS/S2_HARMONIZED")
    .filterBounds(bbox)
    .filterDate("2020-01-01", "2021-01-01")
    .filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", 10))
    )

    moore_after_image = ee.Image(moore_after_collection.first())
    # get info of photos

    moore_after_url = moore_after_image.getThumbURL(
    {
        "format": "png",
        "bands": ["B4", "B3", "B2"],
        "dimensions": [x_dim, y_dim],
        "region": bbox,
        "min": 0,
        "max": 4000,
    }
    ) 

    print(moore_before_url)
    print(moore_after_url)




main()