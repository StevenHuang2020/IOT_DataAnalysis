#Blueburry 06/03/2020
import datetime
import pandas as pd
import numpy as np

from geoDistance import geoDistance
from genPetData import getCsv,getTimeLen
from plotApplication import *

def calculateDistance(df): #per day
    df = df.loc[:,['latitude','longitude']]
    #print(df.head())
    s = 0
    for i in range(df.shape[0]-1):
        #print(i,df.iloc[i,:][0], df.iloc[i,:][1])
        lt,lg = df.iloc[i,:][0],df.iloc[i,:][1]
        nextlt,nextlg = df.iloc[i+1,:][0],df.iloc[i+1,:][1]
        s += geoDistance((lt,lg),(nextlt,nextlg))
    print('total s=', round(s,2), 'meters')
    return round(s,2) #meters
    
def HandleOneDayData(date,dfDay):
    dfDay = dfDay.sort_values(by=['time'],ascending=True)
    #print(dfDay)
    
    sDay = calculateDistance(dfDay)
    #print('Date:',date,'s=',sDay)
    
    weekDay = 0
    start_time = 0
    stop_time = 0
    timeLen = 0
    latitude_center = 0
    longitude_center = 0
    temperature_mean = 0
    distance_day = sDay
    
    firstLine = dfDay.iloc[0,:]
    #print(firstLine,firstLine[0],firstLine[1])
    weekDay = firstLine[2]
    start_time = firstLine[1]
    
    lastLine = dfDay.iloc[-1,:]
    #print(lastLine,lastLine[0],lastLine[1])
    stop_time = lastLine[1]
    
    timeLen = getTimeLen(start_time,stop_time)
    
    temperature_mean = np.mean(dfDay['temperature'])
    latitude_center = np.mean(dfDay['latitude'])
    longitude_center = np.mean(dfDay['longitude'])
    
    columns=['date','weekDay', 'start_time', 'stop_time', 'timeLen', 'latitude_center','longitude_center','temperature_mean','distance_day']
    resDayDf = pd.DataFrame([[date, weekDay, start_time, stop_time,timeLen,latitude_center,longitude_center,temperature_mean,distance_day]], columns=columns)
    #print(resDayDf)
    return resDayDf

def parseAllData():
    file=r'./db/petIotRecordsAll.csv'
    df = getCsv(file,verbose=True)

    #df = df.sort_values(by=['date'],ascending=True)
    dates = list(set(df['date']))
    dates.sort()
    
    dfStatisticDay = pd.DataFrame()
    for i in dates:
        dfDay = df[df['date'] == i]
        print(i,dfDay.shape[0])
        line = HandleOneDayData(i,dfDay)
        dfStatisticDay = dfStatisticDay.append(line,ignore_index=True)
        
    dfStatisticDay.to_csv(r'./db/statistic_result.csv',index=True)
    
def testTracking():
    file=r'./db/' + 'petIotRecordsAll.csv'
    df = getCsv(file)
    
    first = df['date'][0]
    print(first)
    dfFirst = df[df['date'] == first]
    
    distance = calculateDistance(dfFirst)
    if 1:
        trackingPlot(dfFirst,date=first)
        date='2020-05-02'
        trackingPlot(df[df['date'] == date],date=date)
        date='2020-05-03'
        trackingPlot(df[df['date'] == date],date=date)
        date='2020-05-04'
        trackingPlot(df[df['date'] == date],date=date)
        date='2020-05-05'
        trackingPlot(df[df['date'] == date],date=date)
    else:
        dfs = []
        dfs.append(df[df['date'] == '2020-05-01'])
        #dfs.append(df[df['date'] == '2020-05-04'])
        #dfs.append(df[df['date'] == '2020-05-06'])
        trackingCentroidsPlot(dfs,date=first)
        '''
        ax = plt.subplot(1,1,1)
        centroids= [[-36.8542531, 174.76641334], [-36.85011364, 174.76240119], [-36.84837064, 174.74868692]]
        trackingPlotCentroids(ax,centroids)
        
        trackingPlotAx(ax,df)
        plt.tight_layout()
        plt.show()
        '''
        
def main():
    parseAllData()
    testTracking()
    pass

if __name__=='__main__':
    main()
