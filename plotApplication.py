import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from genPetData import getCsv
from plotCommon import *

gRes = r'./res/'
gIndex = 0

def plotModelCSM(modelName,df): #CSM
    x = df.loc[:,['K']].values #K
    csm = df.loc[:,['CSM']]
    
    #plt.figure(figsize=(8,5))
    ax = plt.subplot(1,1,1)
    title = modelName + '_CSM'
    #plt.title(title)
    plotSub(x,csm,ax,label='CSM')
    
    plt.xticks(np.arange(1, 12))
    ax.set_ylabel('Silhouette coefficient')
    ax.set_xlabel('K clusters')
    ax.legend()
    ax.grid()
    plt.savefig(gRes+title+'.png')
    plt.show()
    
def plotModelCSMAx(modelName,ax,df,label='',c='b'): #CSM
    x = df.loc[:,['K']].values #K
    csm = df.loc[:,['CSM']]
    
    #plt.figure(figsize=(8,5))
    #title = modelName + '_CSM'
    #plt.title(title)
    plotSub(x,csm,ax,label=label,c=c)
    
    plt.xticks(np.arange(1, 12))
    ax.set_ylabel('Silhouette coefficient')
    ax.set_xlabel('K clusters')
    
def plotModelTimeTakenAx(modelName,ax,df,label='',c='b'): #CSM
    x = df.loc[:,['K']].values #K
    tt = df.loc[:,['tt(s)']]
    
    #plt.figure(figsize=(8,5))
    #title = modelName + '_CSM'
    #plt.title(title)
    plotSub(x,tt,ax,label=label,c=c)
    
    plt.xticks(np.arange(1, 12))
    ax.set_ylabel('Time taken(s)')
    ax.set_xlabel('K clusters')
    
    
def trackingPlot(df,date='2020-06-01'): ##per day
    ax = plt.subplot(1,1,1)
    trackingPlotAx(ax,df,date,title='Pet tracking'+' ' + date)
    plt.legend()
    plt.subplots_adjust(left=0.18, bottom=None, right=None, top=None, wspace=None, hspace=None)
    plt.grid()
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.savefig(gRes+'locationTracking_'+date+'.png')
    plt.show()
    
def trackingPlotAx(ax,df,date='2020-06-01',title='Pet tracking'):
    df = df.loc[:,['latitude','longitude']]
    #print(df.head())

    lt = df.loc[:,['latitude']].values
    lg = df.loc[:,['longitude']].values
    
    #plt.figure(figsize=(8,5))
    #ax.set_title('Pet tracking'+' ' + date)
    #ax.set_title(title)
    if 1:
        plotSub(lg,lt,ax,label='GPS locations',c='k')
        scatterSub(lg,lt,ax,marker='o',c='b')
    else:
        ax.plot(lg,lt,label='GPS locations',marker='o')
        
    ax.scatter(lg[0],lt[0], c='lightgreen',label='Start',marker='*', edgecolor='black', s=180)
    
def trackingCentroidsPlot(dfs,date='2020-06-01'): ##per day
    ax = plt.subplot(1,1,1)
    
    for df in dfs:
        trackingPlotAx(ax,df,date,title='Pet tracking and Center')
    
    centroids= [[-36.85436064, 174.76640743], [-36.8479573, 174.74841278], [-36.85027437, 174.76268804]]
    #centroids= [[-36.8542531, 174.76641334], [-36.85011364, 174.76240119], [-36.84837064, 174.74868692]]
    trackingPlotCentroids(ax,centroids)
    plt.subplots_adjust(left=0.18, bottom=None, right=None, top=None, wspace=None, hspace=None)
    plt.grid()
    plt.savefig(gRes+'locationTracking_WithCenter_'+date+'.png')
    plt.show()
       
def trackingPlotCentroids(ax,centroids):
    for k,i in enumerate(centroids):
        ax.scatter(i[1],i[0], c='lightgreen',label='Centroid_'+str(k),marker='s', edgecolor='black', s=180)
    ax.legend()
    
def binaryDf(df,labelAdd=True):
    newdf = pd.DataFrame(columns=df.columns)
    #print('pd.shape=',df.shape)
    newIndex = []
    for i in range(df.shape[0]//2):
        dd = df.loc[df.index[i*2], :]
        #print('dd=',df.index[i*2], dd.values)
        if labelAdd:
            newIndex.append(df.index[i*2] +',' + df.index[i*2+1]) #combine
        else:
            newIndex.append(df.index[i*2])#drop
            
        newdf = newdf.append(dd,ignore_index=True)
        
    #print('newIndex=',len(newIndex),newIndex)
    #print('newdf.shape=',newdf.shape)
    newdf.index = newIndex
    return newdf   
    
def plotPdColumn(index,data,title,label,color=None,xlabel='',ylabel='',width=0.6):
    global gIndex
    fontsize = 8
    ax = plt.subplot(1,1,1)
    
    #ax.set_title(title) #,fontsize=fontsize
    #ax.barh(dfWorld.index,dfWorld['Cases'])
    if color:
        ax.bar(index,data,label=label,width=width,color=color)
    else:            
        ax.bar(index,data,label=label,width=width)
        #ax.barh(index,data,label=label)
        
    plt.setp(ax.get_xticklabels(), rotation=30, ha="right",fontsize=fontsize)
    plt.setp(ax.get_yticklabels(),fontsize=fontsize)
    plt.subplots_adjust(left=0.08, bottom=None, right=0.98, top=0.92, wspace=None, hspace=None)
    #plt.yscale("log")
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.subplots_adjust(left=0.12, bottom=None, right=None, top=None, wspace=None, hspace=None)
    plt.savefig(gRes + 'Statistic_' + str(gIndex) +'.png')
    gIndex+=1
    plt.show()

def plotWeekDayDistanceAndTimeLen(df):
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    
    dfStatisticWeekDay = pd.DataFrame()
    for i in weekdays:
        #print(i)
        dfWeekDay = df[df['weekDay'] == i]
        
        weekDay = i
        timeLen = np.mean(dfWeekDay['timeLen'])
        temperature_mean = np.mean(dfWeekDay['temperature_mean'])
        distance_weekday = np.mean(dfWeekDay['distance_day'])
    
        columns=['weekDay', 'timeLen', 'temperature_mean','distance_weekday']
        line = pd.DataFrame([[weekDay, timeLen, temperature_mean, distance_weekday]], columns=columns)
        dfStatisticWeekDay = dfStatisticWeekDay.append(line,ignore_index=True)         
    
    dfStatisticWeekDay['timeLen'] =  dfStatisticWeekDay['timeLen']/60
    
    dfStatisticWeekDay.to_csv(r'./db/statistic_weekday_result.csv',index=True)
    plotPdColumn(dfStatisticWeekDay['weekDay'],dfStatisticWeekDay['timeLen'],title='Pet mean travel time every weekday(miniutes)',label='travel_time',xlabel='WeekDay',ylabel='timeLen(miniutes)',width=0.35)
    #plotPdColumn(dfStatisticWeekDay['weekDay'],dfStatisticWeekDay['temperature_mean'],title='Mean temperature every weekday when pet travel',label='temperature',xlabel='WeekDay',ylabel='temperature')
    plotPdColumn(dfStatisticWeekDay['weekDay'],dfStatisticWeekDay['distance_weekday'],title='Pet mean travel distance every weekday(meters)',label='weekday_distance',xlabel='WeekDay',ylabel='distance(meters)',width=0.35)
    
def plotDateDistanceAndTimeLen(df):
    #df = binaryDf(df,False)
    print(df.shape)
    
    days = df.shape[0]
    if days>30:
        days =30
        
    df = df.iloc[-1*days:,:]
    
    df['timeLen'] =  df['timeLen']/60
    plotPdColumn(df['date'],df['timeLen'],title='Pet travel time every day(miniutes)',label='travel_time',xlabel='Date',ylabel='timeLen(miniutes)')
    plotPdColumn(df['date'],df['distance_day'],title='Pet travel distance every day(meters)',label='travel_distance',xlabel='Date',ylabel='distance(meters)')
    
def plotTempAndDistance(df):
    def HandelTempAndDistance(df,N=2):
        print(df.shape,df.columns)
        df = df.sort_values(by=['temperature_mean'],ascending=True)
        #print(df[:5])
        columns = df.columns
        dfRes = pd.DataFrame()
        for i in range(df.shape[0]//N):
            id = i*N
            #print(i,df.iloc[id,:][0],df.iloc[id,:][1])
            data = df.iloc[id:id+N,:]
            
            temperature = np.mean(data['temperature_mean'])
            distance = np.mean(data['distance_day'])
            line = pd.DataFrame([[temperature, distance]], columns=columns)
            dfRes = dfRes.append(line,ignore_index=True)
            
        return dfRes

    #df = binaryDf(df,False)
    df = df.loc[:,['temperature_mean','distance_day']]
    #df = HandelTempAndDistance(df)
    #print(df)
    print('min=',np.min(df['temperature_mean']),'max=',np.max(df['temperature_mean']))
    
    plot(df['temperature_mean'],df['distance_day'],title='Pet travel Distance vs. temperature ',xlabel='temperature',ylabel='distance(meters)')
    
def plot(x,y,title='',xlabel='',ylabel=''):
    global gIndex
    x = np.linspace(np.min(x),np.max(x),len(y))
    #plt.scatter(x,y)
    #plt.title(title)
    plt.plot(x,y)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(gRes + 'Statistic_' + str(gIndex) +'.png')
    gIndex+=1
    plt.show()
    
def plotAll(df):
    plotDateDistanceAndTimeLen(df)
    plotWeekDayDistanceAndTimeLen(df)
    plotTempAndDistance(df)
    pass

def plotClustering():
    df1 = getCsv('./db/KMeans_result.csv')
    df2 = getCsv('./db/Agglomerative_result.csv')
    #plotModelCSM('A',df1)
    #plotModelCSM('K',df2)
    
    ax = plt.subplot(1,1,1)
    plotModelCSMAx('K',ax,df1,label='K-Means')
    plotModelCSMAx('A',ax,df2,label='Agglomerative',c='r')
    ax.legend()
    ax.grid()
    plt.savefig(gRes+'KA.png')
    plt.show()
    
    ax = plt.subplot(1,1,1)
    plotModelTimeTakenAx('K',ax,df1,label='K-Means')
    plotModelTimeTakenAx('A',ax,df2,label='Agglomerative',c='r')
    ax.legend()
    ax.grid()
    plt.savefig(gRes+'KATt.png')
    plt.show()
    
def plotCLusteringResult(rawData, labels):
    cluster_labels = np.unique(labels)
    print('cluster_labels=',cluster_labels)
    # print(rawData.shape)
    # print(rawData[:5])
    # print(labels.shape)
    # print(labels)
    ax = plt.subplot(1,1,1)
    centroids = []
    for i in cluster_labels:
        lines = np.where(labels == i)
        print(i,len(lines[0].flatten()))
        #print(lines[0])
        data = rawData.iloc[lines[0],:]
        #print(data)
        if 0:
            latitudeCenter = round(np.mean(data['latitude']),8)
            longitudeCenter = round(np.mean(data['longitude']),8)
            x = data['latitude']
            y = data['longitude']
        else:
            latitudeCenter = round(np.mean(data['latitude_center']),8)
            longitudeCenter = round(np.mean(data['longitude_center']),8)
            x = data['latitude_center']
            y = data['longitude_center']
        #ax.scatter(data['latitude_center'],data['longitude_center'])
        
        ax.scatter(x,y)
        ax.scatter(latitudeCenter,longitudeCenter, s=50, c='lightgreen', marker='s', edgecolor='black', label='cluster center'+str(i))    
        # if i==0:
        #     ax.scatter(x,y, s=50, c='lightgreen', marker='s', edgecolor='black', label='cluster 1')    
        # elif i==1:
        #     ax.scatter(x,y, s=50, c='orange', marker='o', edgecolor='black', label='cluster 2')    
        # else:
        #     ax.scatter(x,y, s=50, c='lightblue', marker='v', edgecolor='black', label='cluster 3') 
     
    ax.legend()
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.subplots_adjust(left=0.15, bottom=None, right=None, top=None, wspace=None, hspace=None)
    plt.savefig(gRes+'clusterResut.png')       
    plt.show()    

    
def main():
    df = getCsv('./db/statistic_result.csv')
    #print(df)
    plotAll(df)
    #plotClustering()
    
if __name__=='__main__':
    main()
    