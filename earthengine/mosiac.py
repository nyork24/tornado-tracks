import ee
import numpy as np
import geopy
from geopy import distance
from io import StringIO


service_account = "local-host@ee-tornado-tracks.iam.gserviceaccount.com"
credentials = ee.ServiceAccountCredentials(service_account, r"C:\Users\Lenovo\Downloads\ee-tornado-tracks-ad4d9aafd1a6.json")
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
    
def calculate_before_date(yr, mo, dy, threshold=30):
    """
    Calculate the dates 30 days before and after a given date, returns in YEAR-MO-DY format
    """

    # Create a numpy datetime64 object for the given date
    given_date = np.datetime64(f"{yr:04d}-{mo:02d}-{dy:02d}")
    
    # Calculate 30 days before
    before_date = given_date - np.timedelta64(threshold, 'D')    
    # Format the results as [YEAR-MO-DY]
    before_date_str = str(before_date)
    
    return before_date_str

def calculate_after_date(yr, mo, dy, threshold=14):
    """
    Calculate the dates 30 days before and after a given date, returns in YEAR-MO-DY format
    """
    # Create a numpy datetime64 object for the given date
    given_date = np.datetime64(f"{yr:04d}-{mo:02d}-{dy:02d}")

    # Calculate 30 days after
    after_date = given_date + np.timedelta64(threshold, 'D')    

    # Format the results as [YEAR-MO-DY]
    after_date_str = str(after_date)
    
    return after_date_str

def get_image_dimensions(image):
    """
    Get the dimensions (height and width) of an Earth Engine image.
    
    Args:
        image: ee.Image to analyze.
    
    Returns:
        tuple: (height, width) in pixels.
    """
    # Describe the image
    img_description = ee.Algorithms.Describe(image)
    
    # Get the dimensions from the description
    bands = ee.Dictionary(img_description).get("bands")
    dimensions = ee.List(ee.Dictionary(ee.List(bands).get(0)).get("dimensions"))
    
    # Extract height and width
    print(dimensions)
    height = dimensions.get(0).getInfo()
    width = dimensions.get(1).getInfo()
    
    return height, width


def is_image_blank_or_incomplete(image, region, x_dim, y_dim, scale=30):
    """
    Checks if an image is blank or incomplete by analyzing pixel values.

    Args:
        image: ee.Image to analyze.
        region: ee.Geometry of the area to check.
        scale: Scale in meters for the analysis.
    
    Returns:
        bool: True if the image is blank or incomplete, otherwise False.
    """

    # Get the pixel count in the region
    pixel_count = image.reduceRegion(
        reducer=ee.Reducer.count(),
        geometry=region,
        scale=scale,
        bestEffort = True
        # maxPixels=1e9
    ).getInfo()
    
    # Get the sum of pixel values in all bands
    pixel_sum = image.reduceRegion(
        reducer=ee.Reducer.sum(),
        geometry=region,
        scale=scale,
        bestEffort = True
        # maxPixels=1e9
    ).getInfo()

    # x_dim, y_dim = get_image_dimensions(image)
    
    # Check if all bands have zero or NaN values
    is_blank = all(value == 0 or value is None for value in pixel_sum.values())
    
    # Check if pixel count is below a threshold (indicates incompleteness)
    is_incomplete = bool()
    try:
        dict_values = [value for value in pixel_count.values()]
        print(dict_values)
        print("xdim: " + str(x_dim) + ", ydim: " + str(y_dim) + ", 'checkvalue': " + str((x_dim * y_dim) * 0.85))
        for index in range(13): # iterate through indicies 0-12 (non mask values)
            if dict_values[index - 1] < ((x_dim * y_dim) * 0.85):
                is_incomplete = True
        for index in range(3):  # iterate through indicies 16-18 (non mask values)
            if dict_values[index + 16] < ((x_dim * y_dim) * 0.85):
                is_incomplete = True
    except IndexError:
        is_incomplete = True

    return is_blank or is_incomplete

def fetch_image_with_scaling(image, region, initial_scale=10, max_attempts=10):
    """
    Fetch a satellite image from Google Earth Engine with dynamic scaling to handle size constraints.
    
    Args:
        image: ee.Image object to be requested.
        region: ee.Geometry representing the area of interest.
        initial_scale: Initial resolution scale (in meters per pixel).
        max_attempts: Maximum number of attempts to downscale the image.
    
    Returns:
        ee.Image or None: The image if successful, or None if unable to fetch.
    """
    scale = initial_scale
    attempts = 0

    while attempts < max_attempts:
        try:
            # Try to fetch the image
            url = image.getThumbURL(
            {
                "format": "png",
                "bands": ["B4", "B3", "B2"],
                "scale": scale,
                "region": region,
                "min": 0,
                "max": 3000,
            }
            )
            print(f"Image fetched successfully at scale {scale} meters per pixel.")
            return (url, scale)
        except ee.ee_exception.EEException as e:
            print(f"Request failed at scale {scale}. Retrying with lower resolution...")
            scale *= 2  # Double the pixel size (reduce resolution)
            attempts += 1

    print("Exceeded maximum attempts. Unable to fetch the image.")
    return None

def get_before_image(yr, mo, dy, lat1, lon1, lat2, lon2, max_attempts=5):
    center = get_center(lat1, lon1, lat2, lon2)
    ns = get_ns_km(lat1, lon1, lat2)
    ew = get_ew_km(lat1, lon1, lon2)
    size = (ns, ew)
    x_dim, y_dim = image_dimensions(ns, ew)
    bbox = bbox_from_point(size, center[0], center[1])
    given_date = np.datetime64(f"{yr:04d}-{mo:02d}-{dy:02d}")
    threshold = 30
    attempt = 0
    scale = 10
    url = ""

    while attempt < max_attempts:
        try:
            before_date = calculate_before_date(yr, mo, dy, threshold)
            collection = (
            ee.ImageCollection("COPERNICUS/S2_HARMONIZED")
            .filterBounds(bbox)
            .filterDate(str(before_date), str(given_date))
            .filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", 5))
            )
            image = collection.mosaic()
            fetched_url, fetched_scale = fetch_image_with_scaling(image, bbox, scale)
            print("url ", fetched_url)
            if scale != fetched_scale:
                scale = fetched_scale
                x_dim = x_dim / (scale / 10)
                y_dim = y_dim / (scale / 10)
            if is_image_blank_or_incomplete(image, bbox, x_dim, y_dim, scale) == True:
                raise ValueError
            else:
                print(f"Full image successfully generated at attempt {attempt} at threshold {threshold}.")
                url = fetched_url
                break
        except ValueError:
            attempt += 1
            print(f"Request failed at attempt {attempt}, threshold {threshold}. Retrying at threshold {threshold + 7}...")
            threshold += 7
            before_date = calculate_before_date(yr, mo, dy, threshold)
            print("date ", before_date)


    # while True:
    #     try:
    #         url = image.getThumbURL(
    #         {
    #             "format": "png",
    #             "bands": ["B4", "B3", "B2"],
    #             "dimensions": [x_dim, y_dim],
    #             "region": bbox,
    #             "min": 0,
    #             "max": 3000,
    #         }
    #         )
    #         break
    #     except ee.ee_exception.EEException:
    #         x_dim = x_dim / 1.5
    #         y_dim = y_dim / 1.5
    # url = image.getThumbURL(
    #         {
    #             "format": "png",
    #             "bands": ["B4", "B3", "B2"],
    #             "dimensions": [x_dim, y_dim],
    #             "region": bbox,
    #             "min": 0,
    #             "max": 3000,
    #         }
    #         )    
    return url

def get_after_image(yr, mo, dy, lat1, lon1, lat2, lon2, max_attempts=10):
    center = get_center(lat1, lon1, lat2, lon2)
    ns = get_ns_km(lat1, lon1, lat2)
    ew = get_ew_km(lat1, lon1, lon2)
    size = (ns, ew)
    x_dim, y_dim = image_dimensions(ns, ew)
    bbox = bbox_from_point(size, center[0], center[1])
    given_date = np.datetime64(f"{yr:04d}-{mo:02d}-{dy:02d}")
    threshold = 14
    attempt = 0
    scale = 10
    url = ""

    while attempt < max_attempts:
        try:
            after_date = calculate_after_date(yr, mo, dy, threshold)
            collection = (
            ee.ImageCollection("COPERNICUS/S2_HARMONIZED")
            .filterBounds(bbox)
            .filterDate(str(given_date), str(after_date))
            .filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", 5))
            )
            image = collection.mosaic()
            fetched_url, fetched_scale = fetch_image_with_scaling(image, bbox, scale)
            print("url ", fetched_url)
            if scale != fetched_scale:
                scale == fetched_scale
                x_dim = x_dim / (scale / 10)
                y_dim = y_dim / (scale / 10)
            if is_image_blank_or_incomplete(image, bbox, x_dim, y_dim, scale) == True:
                raise ValueError
            else:
                print(f"Full image successfully generated at attempt {attempt} at threshold {threshold}.")
                url = fetched_url
                break
        except ValueError:
            attempt += 1
            print(f"Request failed at attempt {attempt}, threshold {threshold}. Retrying at threshold {threshold + 7}...")
            threshold += 7
            after_date = calculate_after_date(yr, mo, dy, threshold)
            print("date ", after_date)
    collection = (
    ee.ImageCollection("COPERNICUS/S2_HARMONIZED")
    .filterBounds(bbox)
    .filterDate(str(given_date), str(after_date))
    .filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", 5))
    )
    return url

# def main():
#     center = get_center(33.5995,-95.7490,33.8880,-95.4637)
#     print(center)
#     ns = get_ns_km(33.5995, -95.7490, 33.8880)
#     ew = get_ew_km(33.5995, -95.7490, -95.4637)
#     size = (ns, ew)
#     bbox = bbox_from_point(size, center[0], center[1])

#     x_dim, y_dim = image_dimensions(ns, ew)
#     print(str(x_dim))
#     print(str(y_dim))

#     #downscale image
#     x_dim = int(x_dim / 2)
#     y_dim = int(y_dim / 2)

#     # compact way of storing an ee image collection ?
#     # fix image sizes being too large
#     # add zoom feature if path is large, to highlight specific features
#     before_collection = (
#     ee.ImageCollection("COPERNICUS/S2_HARMONIZED")
#     .filterBounds(bbox)
#     .filterDate("2022-10-01", "2022-11-03")
#     .filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", 5))
#     )

#     before_image = before_collection.mosaic()

    # # getThumbURL ?
    # before_url = before_image.getThumbURL(
    # {
    #     "format": "png",
    #     "bands": ["B4", "B3", "B2"],
    #     "dimensions": [x_dim, y_dim],
    #     "region": bbox,
    #     "min": 0,
    #     "max": 3000,
    # }
    # )   

#     after_collection = (
#     ee.ImageCollection("COPERNICUS/S2_HARMONIZED")
#     .filterBounds(bbox)
#     .filterDate("2022-11-04", "2023-11-07")
#     .filter(ee.Filter.lte("CLOUDY_PIXEL_PERCENTAGE", 5))
#     )

#     after_image = after_collection.mosaic()
#     # get info of photos

#     after_url = after_image.getThumbURL(
#     {
#         "format": "png",
#         "bands": ["B4", "B3", "B2"],
#         "dimensions": [x_dim, y_dim],
#         "region": bbox,
#         "min": 0,
#         "max": 3000,
#     }
#     ) 

#     print(before_url)
#     print(after_url)


def main():
    img_link_before = get_before_image(2022, 3, 5, 41.2334, -94.2013, 41.7340, -93.0135)
    img_link_after = get_after_image(2022, 3, 5, 41.2334, -94.2013, 41.7340, -93.0135)

    print(img_link_before)
    print(img_link_after)


if __name__ == "__main__":
    main()