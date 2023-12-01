import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import ast
import geopy.distance
from data_code.cities_utils import distance_from_cities
import ee
#________________________________________________________________________________
# Distance in miles.Default value = 50 miles 
# Returns demand in Megawatthours
def get_demand_within_distance(latitude,longitude,demand_within_distance=50,unit='km'):
    data_california = pd.read_csv('demand_data_california_with_lat_lon.csv')
    coords_1 = (latitude,longitude)
    demand = 0.
    for ind, row in data_california.iterrows():
        lat = data_california.at[ind,'Latitude']
        lon = data_california.at[ind,'Longitude']
        if not (np.isnan(lat) and np.isnan(lon)):
            coords_2 = (lat,lon)
            if unit=='mile':
            	d = geopy.distance.geodesic(coords_1, coords_2).miles
            elif unit=='km':
            	d = geopy.distance.geodesic(coords_1, coords_2).km
            	
            if d<=demand_within_distance:
                demand += data_california.at[ind,'Sales (Megawatthours)']
                
    demand_from_unidentified_sources = np.sum(data_california[pd.isnull(data_california['Latitude'])]['Sales (Megawatthours)'])
    avg_demand_from_unidentified_sources = demand_from_unidentified_sources/len(data_california[pd.isnull(data_california['Latitude'])])
    
    demand += avg_demand_from_unidentified_sources
    return demand


#________________________________________________________________________________


def get_distance_from_city(lat,long,population_threhold=None,state='CA'):
    """Get distance to the nearest city from a location point.

    Args:
        lat (float): latitude
        long (float): longitude
        population_threhold (int, optional): population threshold to be put on cities. Defaults to None.
        state (str, optional): state under considration. Only cities within this state will be considered. Defaults to 'CA'.

    Returns:
        min_distance: distance to the nearest city (please note that this might not be the true nearest city as the code finds distance to cities sorted by geopraphical radius and stops when the total polpulation reaches a limit which is set to 100000 right now. There might a city further in geography but closer in road distance which might be missed by the code as the code stops before that.)
    """
    distance_list, population_list, city_name_list, city_loc_list = distance_from_cities(lat,long,cities=None,state=state,population_threshold=population_threhold)

    min_distance = sorted(distance_list)[0]

    return min_distance
#_________________________________________________________________________________

ee.Authenticate()
ee.Initialize()
dataset = ee.ImageCollection('USGS/NLCD_RELEASES/2019_REL/NLCD')

def land_cover(longitude, latitude):

    point = ee.Geometry.Point(longitude, latitude)
    nlcd2019 = dataset.filter(ee.Filter.eq('system:index', '2019')).first()
    landcover = nlcd2019.select('landcover')
    landcover_value = landcover.sample(point, scale=30).first().get('landcover').getInfo()
    
    return landcover_value

#_______________________________________________________________________________________
def get_solar_data(latitude, longitude, radius_for_climate_data=100):
    # Returns a dataframe with solar data. 
    # In order to use this function you have to import requests and pandas

    # API Key
    apikey = 'GNoTfD5IZWwIEz24zB5Wn0aEhDvNJSep5bwapzTI'
    parameters = {
        'format': 'json',
        'system_capacity': 1000, # 1000kW = 1 MW, 1 MW or greater is considered utility-scale
        'module_type': 0,       # 0- Standard module, 1- Premium, 2-Thin film
        'losses': 14,           # Losses in percentage
        'array_type': 0,        # Open Rack: Also known as ground mount.
        'tilt': 40,
        'azimuth': 180,         # This means that the solar array is facing South in the Northern Hemisphere
        'lat': latitude,
        'lon': longitude,
        'dataset': 'nsrdb',     # tmy2 is 1960-1990, tmy3 is 1990-2005
        'radius': radius_for_climate_data, # 0-Pick the station nearest to the given (lat,lon), e.g: 50 - 50 miles
        'timeframe': 'monthly',
        'api_key': apikey
    }

    url = 'https://developer.nrel.gov/api/pvwatts/v8'
    response = requests.get(url, params=parameters)
    data = response.json()

    # Check if 'outputs' is in the data
    if 'outputs' not in data:
        print(f"No data available for latitude {latitude} and longitude {longitude}")
        return pd.DataFrame() # Return an empty DataFrame if no data is available

    output_data = data['outputs']
    input_data  = data['inputs']

    output_data['latitude']  = input_data['lat']
    output_data['longitude'] = input_data['lon']

    # Convert output_data to a DataFrame
    df = pd.DataFrame([output_data])
    return df
