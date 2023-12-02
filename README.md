RaPower: Solar Power Plant Location Classifier
================================================

This repository contains an ensemble of machine learning models designed to classify ideal locations for installing utility-scale solar power plants in the state of California. This project represents our submission for the 2023 Erdös Institute Data Science Bootcamp Final Project.

AUTHORS: Utkarsh Agrawal, Mansi Bezbaruah, Harsha Hampapura, Akshay Khadse, Meysam Motaharfar

### Table of Contents
1. [Project Overview](#project-overview)
3. [Data Gathering and Preprocessing](#data-gathering-and-preprocessing)
4. [Modelling Overview](#modelling-overview)
5. [Results and Conclusion](#results-and-conclusion)

## Project Overview
This project is an innovative solution designed to streamline the site selection process 
for utility-scale solar energy farms. Leveraging geospatial data analytics and machine 
learning algorithms, our predictive models assess various factors, including: solar 
irradiance, topography, land use, and population. Then, we provide a recommendation 
system for potential solar power farms, on which our stakeholders can conduct a few 
extra studies before investment and construction. This system significantly reduces 
time and resources spent on research, and thus, is an indispensable tool for our 
stakeholders.

<b> Key Performance Indicator: </b>
How efficiently does the model predict suitable locations compared to actual installations?

## Data Gathering and Preprocessing
Our data consists of 5 features, namely- solar output, land cover data, elevation, slope 
and distance to a nearest city. The solar output tells us about the theoretical maximum 
amount of solar energy that we can harness at this particular location. The elevation 
and slope are indicators of how difficult or easy it would be to build a solar farm. The 
land cover informs us about potential land use restrictions at this place, example, 
open water, or dense forest. Finally, the distance to the nearest city serves as a proxy 
for electricity demand, labor and transportation cost in building the solar farm. 

For plots any of our features on a map please visit [figures](figures).

<b> Cleaning: </b>

To train our classifier model, we also need the formation of places where solar farms cannot 
exist. To this extent, we set thresholds for each feature such that beyond this threshold values, 
it would not be practical to build a utility-scale solar farm. This helped us identify various 
location across California that would serve as examples where solar farms cannot exist. We also
collected a data on a feature called "ac_ouput", which is the theoretical maximum amount of 
solar energy that we can harness at a particular location. 

Our data collection and cleaning code is present in [new_data](new_data) and 
[data_code](data_code). Moreover, all data along with API calls are 
present in [data](data).

## Modelling Overview
Once we had our data cleaned and preprocessed, we plotted density functions for all our features 
and then plotted the features against the ac_output variable. These graphs are present 
[here](data_code/data_viz.ipynb). We observed that the features are 
not Gaussian and don’t show a clear linear or binomial correlation. This helped us eliminate 
certain models. We searched for models that are suitable for a classification task. We chose 
<b> Logistic Regression, Decision Trees, Support Vector Machines, XGBoost Classifiers, and 
Deep Learning with classification layers </b>.

Modelling code, detailed metrics, and confusion matrices are present in [ml_code](ml_code). We
also provide a detailed report [here](ml_code/ML_Model_Report.pdf).

## Results and Conclusion 
As stated above, our goal was to create a model that can classify if a given location 
is suitable for a utility-scale solar farm. After carefully collecting and cleaning 
the data we were able to train models that classify with 95% for the existing solar farms. 
Another observation from our project is the importance of various geographic and 
climatic conditions in building a good solar farm. This can help a shareholder to 
make decisions in case there is a dilemma over building a solar farm based on a 
couple of contradictory features. Surprisingly, we find that all features contribute 
equally to a location being fit for a solar farm. 

### Future Iterations:
There are various ways we can further improve our model. 
1. Adding Features: There are other features that we would like to include in the model
   but we were unable to do so for various reasons. We could include commercial aspects
   such as, land cost, human labor and transportation cost, profit generated, etc into
   the model. Moreover, we would like to quantify measures like government support,
   for example, by introducing a metric and checklist for local laws and incentives
   towards solar energy.
2. Including more locations: Due to time constraints, we had to restrict our data
   collection to the state of California. We could further train and test our model on
   locations outside california. This would increase the accuracy of our models and
   would provide us with more points to test the efficiency index on.


