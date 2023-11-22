import pandas as pd
import requests
import json 
import numpy as np
import matplotlib.pyplot as pl

import os
import pickle
import geopandas as gpd
from shapely.geometry import Polygon, Point


def distance_between(loc1,loc2):

    """
    Finding driving distance
    We use Open Source Routing Machine (OSRM) api to calculate this. 
    http://project-osrm.org/docs/v5.24.0/api/?language=Python#general-options

    input:
        loc1: source location (lat,long)
        loc2: destination location (lat,long)
    output:
        distance: road distance in Km
        duration: time in mins
    """

    r = requests.get(f"""http://router.project-osrm.org/route/v1/car/{loc1[1]},{loc1[0]};{loc2[1]},{loc2[0]}?overview=false""")
    # print(r.content)
    try: 
        content = json.loads(r.content)['routes'][0]
    except: 
        print(r.content)
        return False
    distance,duration = content['distance'],content['duration']

    return distance/1000, duration/60



def get_city_data():
    """Returns pandas dataframe for US cities with columns: 'city','state_id','state_name','county_name','lat','lng','population','density'

    Returns:
        data: pandas dataframe
    """

    final_file = '../data/cities_data/simplemaps_uscities_basicv1.76/uscitites_clean.csv'
    if os.path.isfile(final_file):
        with open(final_file,'rb') as f:
            data = pickle.load(f)
        return data
    
    file_name = 'cities_data/simplemaps_uscities_basicv1.76/uscities.csv'
    city_data = pd.read_csv(file_name)
    required_cols = ['city','state_id','state_name','county_name','lat','lng','population','density']
    city_data_filtered = city_data.filter(required_cols,axis=1)
    with open(final_file,'wb') as f:
        pickle.dump(city_data_filtered,f)
    return city_data_filtered




def state_polygon(state_name):
    """Returns Polygon of a US state

    Args:
        state_name (str): US state name

    Returns:
        polygon: Polygon for the state boundary
    """
    boundaries = pd.read_csv('../data/cities_data/us-state-boundaries.csv',sep=';')
    assert state_name in boundaries['name'].values, "State not in the list"
    
    boundaries = boundaries.filter(['name','St Asgeojson'],axis=1)
    state = json.loads((boundaries.loc[boundaries['name']==state_name]).values[0][1])
    polygon = Polygon(state['coordinates'][0][0])
    return polygon


def state_grid(state_name,resolution):
    """creates grid of points inside the state

    Args:
        state_name (str): name of the US state
        resolution (float): distance resolution for the grid (units of miles)
    output:
        valid_points: list of (latitude,longitude) of points inside the state
    """

    polygon = state_polygon(state_name)
    

    ## Creating grid points inside the state
    x_min,y_min,x_max,y_max = polygon.bounds
    lat_dist_per_degree = 111/1.6 #in miles
    long_dist_per_degree = np.cos((y_min+y_max)*0.5)*111/1.6 #in miles
    resolution_lat = resolution/lat_dist_per_degree
    resolution_long = resolution/long_dist_per_degree
    gridx_points = np.arange(x_min,x_max,resolution_long)
    gridy_points = np.arange(y_min,y_max,resolution_lat)

    valid_points = []
    invalid_points = []
    for x in gridx_points:
        for y in gridy_points:
            # print(Point(x,y).within(polygon))
            if Point(x,y).within(polygon):
                valid_points.append((x,y))
            else:
                invalid_points.append((x,y))
    return valid_points, polygon



def distance_from_cities(cities,lat,lng):
    """Generate driving distance of a point from major cities in a state

    Args:
        cities: pandas dataframe containing coordinates of the city which are included in the search list
        lat (float): latitude of the location 
        lng (float): longitude of the location
        radii (float, optional): Threshold for the distance in miles. Defaults to None. This is obsolete in the current version

    Returns:
        distance_list: distance of to all cities within the radii
        population_list: population of cities within the radii
    """
    distance_list = []
    population_list = []
    city_name_list = []
    city_loc_list = []
    totol_pop = 0

    # if radii is None:
    #     radii = 100000000 # some random value which is not possible in physical scenario
    # lat_radii = radii/(111/1.6) # in miles
    # lng_radii = abs(radii/(111*np.cos(lat)/1.6)) #in miles
    
    city_locs = cities[['lng','lat']].values
    city_names = cities['city'].values
    city_pop = cities['population'].values
    
    
    dist_in_degrees = np.abs(city_locs - np.array([lng,lat]).reshape((1,2)))
    dist_in_degrees = np.sum(np.abs(dist_in_degrees[:]),axis=-1)    
    sorted_indices = dist_in_degrees.argsort()

    # sorting cities according to the distance from the location
    city_locs = city_locs[sorted_indices]
    city_names = city_names[sorted_indices]
    city_pop = city_pop[sorted_indices]

    # for index,city in cities.iterrows():
    for i,city in enumerate(city_locs):

        city_lng,city_lat = city[0],city[1]
        result = distance_between((lat,lng),(city_lat,city_lng))
        if not result:
            return False
        else:
            dist,_ = result
        distance_list.append(dist)
        city_loc_list.append((city_lat,city_lng))
        city_name_list.append(city_names[i])
        population_list.append(city_pop[i])
        totol_pop += population_list[-1]
        if totol_pop > 100000: # this is some random number. We can also break the loop when we find the first city. But then the distance we find might not be the shortest distance to city. Relaxing this criteria increase the runtime.
            break
    
    index = list(range(len(distance_list)))
    index = sorted(index,key=lambda x:distance_list[x])
    distance_list = [distance_list[x] for x in index]
    population_list = [population_list[x] for x in index]
    city_loc_list = [city_loc_list[x] for x in index]
    city_name_list = [city_name_list[x] for x in index]

    return distance_list, population_list, city_name_list, city_loc_list