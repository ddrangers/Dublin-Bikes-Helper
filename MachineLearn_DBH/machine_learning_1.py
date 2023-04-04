
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates
import requests
import json
from pathlib import Path
import time
import datetime
from datetime import datetime
import sys

## Function to convert day number to day
def convert_day(num):
    if num == 0:
        return 'Monday'
    elif num == 1:
        return 'Tuesday'
    elif num == 2:
        return 'Wednesday'
    elif num == 3:
        return 'Thursday'
    elif num == 4:
        return 'Friday'
    elif num == 5:
        return 'Saturday'
    else:
        return 'Sunday'
    
## Function to convert Month number to Month
def convert_month(num):
    if num == 1:
        return 'January'
    elif num == 2:
        return 'February'
    elif num == 3:
        return 'March'
    elif num == 4:
        return 'April'
    elif num == 5:
        return 'May'
    elif num == 6:
        return 'June'
    elif num == 7:
        return 'July'
    elif num == 8:
        return 'August'
    elif num == 9:
        return 'September'
    elif num == 10:
        return 'October'
    elif num == 11:
        return 'November'
    else:
        return 'December'
    
#path to file and Read File
file_path_csv = Path('C:\\Users\\corma\\Documents\\GitHub\\Dublin-Bikes-Helper\\MachineLearn_DBH\\bike_info.csv')
#file_path_csv = Path('C:\\Users\\corma\\Desktop\\Software Eng\\dublinbikes_20211001_20220101_usage.csv')
df = pd.read_csv(file_path_csv)
df.head()

#Set up Time elements
df["TIME"] = pd.to_datetime(df["creat_time"],format='%d/%m/%Y %H:%M')

#Set up Day elements
df['Day_of_Week'] = df['TIME'].dt.dayofweek
df["DAY_num"] = df["TIME"].dt.day
df.loc[df['Day_of_Week'] == 0, 'DAY'] = 'Mon'  
df.loc[df['Day_of_Week'] == 1, 'DAY'] = 'Tue'  
df.loc[df['Day_of_Week'] == 2, 'DAY'] = 'Wed'  
df.loc[df['Day_of_Week'] == 3, 'DAY'] = 'Thu'  
df.loc[df['Day_of_Week'] == 4, 'DAY'] = 'Fri' 
df.loc[df['Day_of_Week'] == 5, 'DAY'] = 'Sat' 
df.loc[df['Day_of_Week'] == 6, 'DAY'] = 'Sun' 

#Set up other Time elements
df["YEAR"] = df["TIME"].dt.year
df["MONTH"] = df["TIME"].dt.month
df["HOUR"] = df["TIME"].dt.hour
df["MINUTE"] = df["TIME"].dt.minute
#df['Time'].head()

#Check BIke availability or Bike Parking Availability
req = input("Do you want to check for Bike Availability (Type: b) or Parking Availability (Type: p): ")
if req == 'b' or req == 'B' or req == 'p' or req == 'P' or req == 'bike' or req == 'Bike' or req == 'park' or req == 'Park':

## Set up Search Parameters (Station ID, Day) 
    month_num = 3

    #Day of the week
    day_num = int(input("Enter Day Number (1 = Mon, 2 = Tues, 3 = Wed etc): "))
    #Minute pass the hour
    #min_num = int(input("Enter Minute pass the hour (0 - 15 - 30 - 45): "))
    
    #Station ID
    stationid = int(input("Enter Station ID (1 to 117): "))

    try:
        stationname = df.loc[(df['number']==stationid),'name'].values[0]

        #Filter data based on certain input parameters
        df['station_select'] = (df['YEAR']==2023) & (df['MONTH']==month_num) & (df['Day_of_Week']==day_num-1) & (df['number']==stationid)

        ## Set up x- and y-axis of Plot
        x =df['HOUR'].loc[df['station_select']]

        if req == 'bike' or req == 'Bike' or req == 'b' or req == 'B':
            y = df['bike_available'].loc[df['station_select']]
            plt.ylabel("Bike Availability")
            plt.title(f'Likely Bike Availability \nfor {stationname} \non {convert_day(day_num-1)}')
        elif req == 'park' or req == 'Park' or req == 'p' or req == 'P':
            y = df['bike_stand_available'].loc[df['station_select']]
            plt.ylabel("Bike Parking Availability")
            plt.title(f'Likely Bike Parking Availability \nfor {stationname} \non {convert_day(day_num-1)}')

        #Set Up Plot
        plt.xlabel("Time (24 hours)")
        #c=['blue','blue','blue','blue','blue','blue','blue','blue','red','red','red','red','red','red','red','red','red','red','blue','blue','blue','blue','blue','blue']
        ytick = np.array([0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,44])
        xtick = np.array([0,4,8,12,16,20,24])
        plt.xticks(xtick)
        plt.yticks(ytick)
        plt.xlim(0,24)
        plt.bar(x,y)
        plt.show()
    except:
        print ("Station ID Does not exist")
    
else:
    print("Incorrect Entry")