import ee

service_account = "local-host@ee-tornado-tracks.iam.gserviceaccount.com"
credentials = ee.ServiceAccountCredentials(service_account, r"C:\Users\Lenovo\Github-Projects\earth-engine-api-key.json")
ee.Initialize(credentials)

def get_center(lat1, lon1, lat2, lon2):
    center_lat = (lat1 + lat2) / 2
    center_lon = (lon1 + lon2) / 2
    return (center_lat, center_lon)


# coordinates = 
# point = ee.Geometry.Point()

def main():
    print(get_center(35.284,-97.628,35.341,-97.3999))

main()
    