import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import ast
import geopy.distance
from data_code.cities_utils import distance_from_cities
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