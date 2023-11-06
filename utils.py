import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json
import ast
import geopy.distance

#________________________________________________________________________________
# Distance in miles.Default value = 50 miles 
# Returns demand in Megawatthours
def get_demand_within_distance(latitude,longitude,demand_within_distance=50):
    coords_1 = (latitude,longitude)
    demand = 0.
    for ind, row in data_california.iterrows():
        lat = data_california.at[ind,'Latitude']
        lon = data_california.at[ind,'Longitude']
        if not (np.isnan(lat) and np.isnan(lon)):
            coords_2 = (lat,lon)
            d = geopy.distance.geodesic(coords_1, coords_2).miles
            if d<=demand_within_distance:
                demand += data_california.at[ind,'Sales (Megawatthours)']
                
    demand_from_unidentified_sources = np.sum(data_california[pd.isnull(data_california['Latitude'])]['Sales (Megawatthours)'])
    avg_demand_from_unidentified_sources = demand_from_unidentified_sources/len(data_california[pd.isnull(data_california['Latitude'])])
    
    demand += avg_demand_from_unidentified_sources
    return demand


#________________________________________________________________________________