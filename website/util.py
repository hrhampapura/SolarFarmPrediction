import json
import pickle
import numpy as np
import pandas as pd

__model_lr = None
__model_tree = None
__model_svm = None


def get_slope_from_lat_lon(lat, lon):
	# Function to be added later
	x = [8.00000000e+00, 8.30000000e+01, 1.00000000e+00, 1.58973973e+06,3.03885000e+01]
	slope,elevation,land_cover,ac_annual,min_distance = np.array(x)
	return slope

def get_elevation_from_lat_lon(lat, lon):
	# Function to be added later
	x = [8.00000000e+00, 8.30000000e+01, 1.00000000e+00, 1.58973973e+06,3.03885000e+01]
	slope,elevation,land_cover,ac_annual,min_distance = np.array(x)
	return elevation

def get_land_cover_from_lat_lon(lat,lon):
	# Function to be added later
	x = [8.00000000e+00, 8.30000000e+01, 1.00000000e+00, 1.58973973e+06,3.03885000e+01]
	slope,elevation,land_cover,ac_annual,min_distance = np.array(x)
	return land_cover

def get_ac_annual_from_lat_lon(lat,lon):
	# Function to be added later
	x = [8.00000000e+00, 8.30000000e+01, 1.00000000e+00, 1.58973973e+06,3.03885000e+01]
	slope,elevation,land_cover,ac_annual,min_distance = np.array(x)
	return ac_annual

def get_min_distance_from_lat_lon(lat,lon):
	# Function to be added later
	x = [8.00000000e+00, 8.30000000e+01, 1.00000000e+00, 1.58973973e+06,3.03885000e+01]
	slope,elevation,land_cover,ac_annual,min_distance = np.array(x)
	return min_distance

def get_features_from_lat_lon(lat, lon):
    slope      = get_slope_from_lat_lon(lat, lon)
    elevation  = get_elevation_from_lat_lon(lat, lon)
    land_cover = get_land_cover_from_lat_lon(lat,lon)
    ac_annual  = get_ac_annual_from_lat_lon(lat,lon)
    min_distance = get_min_distance_from_lat_lon(lat,lon)
    
    feature_list = [slope, elevation, land_cover, ac_annual, min_distance]
    return feature_list


def classify_solar_site(lat,lon,model):
    
    features_list = get_features_from_lat_lon(lat, lon)
    slope,elevation,land_cover,ac_annual,min_distance = np.array(features_list)
    dict_ = {'slope':[slope], 'elevation':[elevation], 'land_cover':[land_cover],
             'ac_annual':[ac_annual], 'min_distance':[min_distance]}

    features = pd.DataFrame.from_dict(dict_)
    
    if model=='Logistic_Regression':
        estimator = __model_lr
    elif model=='Decision_Tree':
        estimator = __model_tree
    elif model=='Support_Vector_Machine':
        estimator = __model_svm
        
    # # Access the best model with its hyperparameters
    best_model = estimator.best_estimator_

    # Make predictions
    classification = best_model.predict(features) 
    
    return classification


def load_saved_artifacts():
	print("loading saved artifacts...start")
	global __model_lr
	global __model_tree
	global __model_svm

	with open("./artifacts/lr.pkl",'rb') as f:
		__model_lr = pickle.load(f)

	with open("./artifacts/decision_tree.pkl",'rb') as f:
		__model_tree = pickle.load(f)

	with open("./artifacts/svm.pkl",'rb') as f:
		__model_svm = pickle.load(f)

	print("loading saved artifacts...done")


if __name__=="__main__":
	load_saved_artifacts()
	print(classify_solar_site(3,4,'Logistic_Regression'))
	print(classify_solar_site(3,4,'Decision_Tree'))
	print(classify_solar_site(3,4,'Support_Vector_Machine'))
