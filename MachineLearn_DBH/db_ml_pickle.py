#Import Modules
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates
from pathlib import Path
import sys
import pickle

import time
from datetime import datetime
import datetime

from sklearn.linear_model import LinearRegression
from sklearn import metrics
from sklearn.model_selection import train_test_split, cross_validate, cross_val_score, RandomizedSearchCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import datasets, linear_model
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Lasso
from sklearn.tree import export_graphviz
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score, recall_score, ConfusionMatrixDisplay
from sklearn.ensemble import RandomForestRegressor
from scipy.stats import randint
from sklearn import tree

#path to files
file_path_csv_weather = Path('C:\\Users\\corma\\Documents\\GitHub\\Dublin-Bikes-Helper\\MachineLearn_DBH\\weather_info_final.csv')
file_path_csv_bike = Path('C:\\Users\\corma\\Documents\\GitHub\\Dublin-Bikes-Helper\\MachineLearn_DBH\\bike_info_final.csv')
file_path_pickle = Path('C:\\Users\\corma\\Documents\\GitHub\\Dublin-Bikes-Helper\\MachineLearn_DBH\\Pickle Files\\')
#Read files and create Dataframes
df = pd.read_csv(file_path_csv_bike,index_col=False)
dfw = pd.read_csv(file_path_csv_weather,index_col=False)

#Convert Temperature from Kelvin to Celcius and weather_main to number representation
dfw["tempcel"] = dfw["temp"]-273.15
dfw["tempcel_feel"] = dfw["temp_feel"]-273.15
dfw['weather_main'].replace(['Clouds', 'Rain','Snow','Clear','Drizzle','Mist','Fog'],[2, 4,5,1,3,6,7], inplace=True)

#Setup All Time Parameters - Bike Data
df["TIME"] = pd.to_datetime(df["creat_time"],format='%Y-%m-%d %H:%M:%S')
df["YEAR"] = df["TIME"].dt.year
df["MONTH"] = df["TIME"].dt.month
df["DAY"] = df['TIME'].dt.dayofweek
df["DAY_num"] = df["TIME"].dt.day
df["HOUR"] = df["TIME"].dt.hour
df["MINUTE"] = df["TIME"].dt.minute
df['TIME'] = df['TIME'].dt.round('H')

#Setup All Time Parameters - Bike Data
dfw["TIME"] = pd.to_datetime(dfw["creat_time"],format='%Y-%m-%d %H:%M:%S')
dfw["sunrise"] = pd.to_datetime(dfw["sunrise"],format='%Y-%m-%d %H:%M:%S')
dfw["sunset"] = pd.to_datetime(dfw["sunset"],format='%Y-%m-%d %H:%M:%S')
dfw["YEAR"] = dfw["TIME"].dt.year
col =np.array(dfw["YEAR"],np.int64) #Converts float to int
dfw["YEAR"] = col #Converts float to int
dfw["MONTH"] = dfw["TIME"].dt.month
col =np.array(dfw["MONTH"] ,np.int64)
dfw["MONTH"]  = col
dfw['DAY'] = dfw['TIME'].dt.dayofweek
col =np.array(dfw['DAY'],np.int64) 
dfw['DAY'] = col 
dfw["DAY_num"] = dfw["TIME"].dt.day
col =np.array(dfw["DAY_num"],np.int64)
dfw["DAY_num"] = col
dfw["HOUR"] = dfw["TIME"].dt.hour
col =np.array(dfw["HOUR"] ,np.int64)
dfw["HOUR"]  = col
dfw["MINUTE"] = dfw["TIME"].dt.minute
col =np.array(dfw["MINUTE"] ,np.int64)
dfw["MINUTE"] = col
dfw['TIME'] = dfw['TIME'].dt.round('H')

#Combine both Dataframes
dfbikeweath = pd.merge(df, dfw, on='TIME', how='inner')

#Split Data Set into Training and Test Set
train_set,test_set = train_test_split(dfbikeweath,test_size=0.2,random_state=42)

#Create New Lists for holding results of Model Runs
randommodel_mser_train_list = []
randommodel_mser_test_list = []
randommodel_stationid = []

#Choose whether to predict bike availability or parking availability
bikeprediction = False
if bikeprediction == True:
    predict = 'bike_available'
    fileappend = 'bike'
else:
    predict = 'bike_stand_available'
    fileappend = 'park'

for i in range(1,120):
    #day_num = 5  #Thursday
    stationid = i
    try:
        #Value we are trying to predict (y) - Bike Availability or Bike Parking - at Station = stationid
        #For each station
        
        train_set['station_select'] = (train_set['number']==stationid)
        #train_set['station_select'] = (train_set['YEAR_y']==2023) & (train_set['MONTH_y']==3) & (train_set['number']==stationid)

        y = train_set[predict].loc[train_set['station_select']]

        #Weather parameters (X) we are using for prediction of Bike Availability
        features = ['weather_main','clouds','tempcel', 'weather_id', 'wind_speed','tempcel_feel','MONTH_x','DAY_x','HOUR_x']

        #Use Random Forest as prediction model
        X = train_set[features].loc[train_set['station_select']]
        randomforest = RandomForestRegressor()
        randomforest.fit(X, y)
        randomforest_predictions = randomforest.predict(X).round(0)

        #Test the model on the Test Set
        test_set['station_select'] = (test_set['number']==stationid)
        #test_set['station_select'] = (test_set['YEAR_y']==2023) & (test_set['MONTH_y']==3) & (test_set['number']==stationid)
        y_test = test_set[predict].loc[test_set['station_select']]
        X_test = test_set[features].loc[test_set['station_select']]
        randomforest_predictions_test = randomforest.predict(X_test).round(0)

        #Calculate R2 for Training Set and Test Set Data
        randomforest_mse = mean_squared_error(y,randomforest_predictions)
        randomforest_mser = np.sqrt(randomforest_mse).round(2)
        randomforest_mse_test = mean_squared_error(y_test,randomforest_predictions_test)
        randomforest_mser_test = np.sqrt(randomforest_mse_test).round(2)
        randommodel_mser_test_list.append(randomforest_mser_test)
        randommodel_mser_train_list.append(randomforest_mser)
        randommodel_stationid.append(stationid)
    
        # Serialize model object (in this case Random Forest) into a file and send to disk using pickle
        filename = f'{file_path_pickle}\\randomforest{stationid}_{fileappend}.pkl'
        print(filename)
        with open(filename, 'wb') as handle:
            pickle.dump(randomforest, handle, pickle.HIGHEST_PROTOCOL)
    except:
        print(f'No Station with ID number {i} exists')
#Print out the results
results_file = f'{file_path_pickle}\\R2_randomforest_{fileappend}.txt'
with open(results_file,'a') as f:
    f.write(f'R2 Comparisons (Training vs Test Set) for stations: {fileappend} predictions \n---------------------------------------------------------------------')
        
for i in range(len(randommodel_stationid)):
    print(f'\nFor station: {randommodel_stationid[i]} | R2 (Training) = {randommodel_mser_train_list[i]} -- R2 (Test) = {randommodel_mser_test_list[i]}')
    with open(results_file,'a') as f:
         f.write(f'\nFor station: {randommodel_stationid[i]} | R2 (Training) = {randommodel_mser_train_list[i]} -- R2 (Test) = {randommodel_mser_test_list[i]}')
        
