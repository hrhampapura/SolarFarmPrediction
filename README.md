RaPower: Solar Power Plant Location Classifier
================================================

This is a Machine Learning model that classifies ideal locations to install utility-scale solar 
power plant in the state of California. This project is our submission for the 2023 Erdös 
Institute Data Science Bootcamp Final Project. 

AUTHORS: Utkarsh Agrawal, Mansi Bezbaruah, Harsha Hampapura, Akshay Khadse, Meysam Motaharfar

### Table of Contents
1. [Project Overview](#project-overview)
3. [Data Gathering and Preprocessing](#data-gathering-and-preprocessing)
4. [Modelling Overview](#modelling-overview)
5. [Results and Conclusion](#results-and-conclusion)

## Project Overview
Solar power is crucial in addressing the escalating global energy crisis and mitigating 
environmental degradation. As a renewable and inexhaustible resource, solar energy offers 
a sustainable alternative to finite fossil fuels. With advances in technology, more 
governements and utility providers have started investing in solar farms. As such, 
it becomes imperative to optimize the site selection of utility-scale solar farms.
Here, utility scale means all farms that produce over 1Mw of power.

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


<b> Parameters and Collection: </b>

We obtained the data for existing utility-scale solar farms using the Large-Scale Solar 
Photovoltaic Database provided on the United States Geological Survey website.  We then 
focused on the data in California. As indicators of a good location for building a 
utility-scale solar farm we decided on 5 main features namely - solar output, 
land cover data, elevation, slope and distance to a nearest city. The solar output 
tells us about the theoretical maximum amount of solar energy that we can harness 
at this particular location. The elevation and slope are indicators of how difficult 
or easy it would be to build a solar farm. The land cover informs us about potential 
land use restrictions at this place, example, open water, or dense forest. 
And finally the distance to the nearest city serves as a proxy for electricity demand, 
labor and transportation cost in building the solar farm. 

<b> Data Sources: </b>

1. NREL: https://developer.nrel.gov/docs/solar/nsrdb/python-examples/
2. USGS Land Use, Topography and Geological Factors Data Sets
3. Approximate AC Output: https://solargis.com/docs/getting-started/why-solargis
4. Google Earth Project SunRoof: https://sunroof.withgoogle.com
5. Open Source Routing Machine: http://project-osrm.org/
6. Harmonised global dataset of solar farms: https://www.nature.com/articles/s41597-020-0469-8

<b> Cleaning: </b>

To train our classifier model, we also need the formation of places where solar farms cannot 
exist. To do this we set thresholds for each feature such that beyond this threshold values, 
it would not be practical to build a utility-scale solar farm. This helped us identify various 
location across California that would serve as examples where solar farms cannot exist.

## Modelling Overview
Once we had our data cleaned and preprocessed, we plotted density functions for all our features 
and then plotted the features against the AC output variable. We observed that the features are 
not gaussian and don’t show a clear linear or binomial correlation. This helped us eliminate 
certain models like Naive Bayes and Linear Regression. Moreover, we searched for models that 
are suitable for a classification task. We chose Logistic Regression, Decision Trees, 
Support Vector Machines, XGBoost Classifiers, and Deep Learning with classification layers.

## Results and Conclusion 

