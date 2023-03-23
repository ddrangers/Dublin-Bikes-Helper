
import pandas as pd
import numpy as np
#%matplotlib inline
import matplotlib.pyplot as plt
import matplotlib.dates
import requests
import json
from pathlib import Path
import time
import datetime
import sys

## Function to convert day number to day
def convert_day(num):
    if num == 1:
        return 'Monday'
    elif num == 2:
        return 'Tuesday'
    elif num == 3:
        return 'Wednesday'
    elif num == 4:
        return 'Thursday'
    elif num == 5:
        return 'Friday'
    elif num == 6:
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
file_path_csv = Path('C:\\Users\\corma\\Desktop\\Software Eng\\dublinbikes_20211001_20220101_usage.csv')
df = pd.read_csv(file_path_csv)

#Set up Time elements
df["TIME"] = pd.to_datetime(df["TIME"])
df["DAY_num"] = df["TIME"].dt.day
df.loc[df['DAY_num'] == 1, 'DAY'] = 'Mon'  
df.loc[df['DAY_num'] == 2, 'DAY'] = 'Tue'  
df.loc[df['DAY_num'] == 3, 'DAY'] = 'Wed'  
df.loc[df['DAY_num'] == 4, 'DAY'] = 'Thu'  
df.loc[df['DAY_num'] == 5, 'DAY'] = 'Fri' 
df.loc[df['DAY_num'] == 6, 'DAY'] = 'Sat' 
df.loc[df['DAY_num'] == 7, 'DAY'] = 'Sun' 
df["YEAR"] = df["TIME"].dt.year
df["MONTH"] = df["TIME"].dt.month
df["HOUR"] = df["TIME"].dt.hour
df["MINUTE"] = df["TIME"].dt.minute

#Check BIke availability or Bike Parking Availability
req = input("Do you want to check for Bike Availability (Type: bike) or Parking Availability (Type: park): ")
if req == 'bike' or req == 'Bike' or req == 'park' or req == 'Park':

    ## Set up Search Parameters (Station ID, Day) 
    month_num = 10

    #Day of the week
    day_num = int(input("Enter Day Number (1 = Mon, 2 = Tues etc): "))
    #Minute pass the hour
    #min_num = int(input("Enter Minute pass the hour (0 - 15 - 30 - 45): "))
    #Station ID
    stationid = int(input("Enter Station ID (1 to 113): "))

    try:
        stationname = df.loc[(df['STATION ID']==stationid),'NAME'].values[0]

        #Filter data based on certain input parameters
        df['station_select'] = (df['YEAR']==2021) & (df['MONTH']==month_num) & (df['DAY_num']==day_num) & (df['MINUTE']==45) & (df['STATION ID']==stationid)

        ## Set up x- and y-axis of Plot
        x =df['HOUR'].loc[df['station_select']]
        if req == 'bike' or req == 'Bike':
            y = df['AVAILABLE BIKES'].loc[df['station_select']]
            plt.ylabel("Bike Availability")
            plt.title(f'Likely Bike Availability \nfor {stationname} \non a {convert_day(day_num)}')
        elif req == 'park' or req == 'Park':
            y = df['AVAILABLE BIKE STANDS'].loc[df['station_select']]
            plt.ylabel("Bike Parking Availability")
            plt.title(f'Likely Bike Parking Availability \nfor {stationname} \non {convert_day(day_num)}')

        #Set Up Plot
        plt.xlabel("Time (24 hours)")
        c=['blue','blue','blue','blue','blue','blue','blue','blue','red','red','red','red','red','red','red','red','red','red','blue','blue','blue','blue','blue','blue']
        ytick = np.array([0, 2, 4, 6,8,10,12,14,16,18,20,22,24,26,28,30])
        xtick = np.array([0, 4, 8, 12,16,20,24])
        plt.xticks(xtick)
        plt.yticks(ytick)
        plt.xlim(0,24)
        plt.bar(x,y,color=c)
        plt.show()

    except:
        print ("Station ID Does not exist")
    
else:
    print("Incorrect Entry")