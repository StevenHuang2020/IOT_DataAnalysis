#Blueburry 06/03/2020
import datetime
import pandas as pd
import numpy as np

def getDate():
    daytime = datetime.datetime.now()
    today = datetime.date.today()
    #t = str(today) + '_' + str(daytime.__format__('%H%M%S'))
    return str(today) ##2020-06-03

def getTime():
    daytime = datetime.datetime.now()
    return str(daytime.__format__('%H:%M:%S')) #17:01:38

def getTimeLen(startTime,stopTime):#17:01:38
    start = datetime.datetime.strptime(startTime,'%H:%M:%S')
    stop = datetime.datetime.strptime(stopTime,'%H:%M:%S')
    total = (stop-start).total_seconds()  #seconds
    #print(total)
    return total

def getRandomLenFromDate(date,N=200):
    date = datetime.datetime.strptime(date,'%Y-%m-%d')
    weekDay = datetime.datetime.strftime(date,'%A')
    weekdays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    values = [0.2, 0.15, 0.2, 0.3, 0.32, 0.5, 0.6 ]
    index = weekdays.index(weekDay)
    len = int((values[index] + randomSymbol(1)*noise(b=0.12))*N)
    print('len=',len)
    return len

def getRandomTempFromDate(date,N=5):
    date = datetime.datetime.strptime(date,'%Y-%m-%d')
    days = datetime.datetime.strftime(date,'%j')
    
    values = [0.2, 0.4, 0.2, 0.3, 0.32, 0.4, 0.5 ]
    index = int(days)%len(values)
    temp = values[index]*N
    #print('temp=',temp)
    return temp

def randomSymbol(length): #-1,1,1,-1,1,-1...
    return np.zeros(length)+np.where(np.random.random(length)>0.5,1.0,-1.0)
    
def noise(N=1,a=0,b=5): #[a,b]
    #return np.random.rand(1)
    return np.random.random((N,))*(b-a) + a

    # x = np.random.normal(loc=b,scale=0.005,size=(N,)) #scale=0.0005
    # print('mean,var,min,max=',np.mean(x),np.var(x),np.min(x),np.max(x))
    # return x

def writeToCsv(df,file):
    df.to_csv(file,index=True)

def getCsv(file,header=0,verbose=False):
    df = pd.read_csv(file,header=header)
    if verbose:
        print(df.describe().transpose())
        print(df.dtypes)
        print(df.columns)
        print(df.head())
    print('dataset=', df.shape)    
    return df  
 
def genDataTime(N=10,date=getDate(),startT=getTime(),inter=5):
    d = date
    t = startT
    
    sDate=datetime.datetime.strptime(d,'%Y-%m-%d')
    sWeekDay = datetime.datetime.strftime(sDate, '%A')#sDate.weekday()
    sTime=datetime.datetime.strptime(t,'%H:%M:%S')
    #print('sDate,sWeekDay,sTime=',sDate,sWeekDay,sTime)
    dates,weekdays,times = [],[],[]
    for i in range(N):
        dates.append(d)
        times.append(t)
        weekdays.append(sWeekDay)
        
        #d = sDate + datetime.timedelta(days=(i+1)*1)
        #d = datetime.datetime.strftime(d,'%Y-%m-%d')
        t = sTime + datetime.timedelta(seconds=(i+1)*inter)
        t = datetime.datetime.strftime(t,'%H:%M:%S')
        #print('d,t=',d,t)
    return dates,weekdays,times

def genLocation(N,u=0.006):
    # startLat=-36.854265
    # startLg=174.766519
    pts = [[-36.854265, 174.766519],
           [-36.850265, 174.762519],
           [-36.848265, 174.748519]]
    
    pt = pts[np.random.randint(len(pts))]
    startLat = pt[0]
    startLg = pt[1]
    #print('startLat,startLg=',startLat,startLg)
    
    latitude,longitude = [],[]
    latitude.append(startLat)
    longitude.append(startLg)
    for i in range(N-1):
        la = latitude[-1] + noise(N=1,a=-1*u, b=u).flatten()[0]
        lg = longitude[-1] + noise(N=1,a=-1*u, b=u).flatten()[0]
        latitude.append(la)
        longitude.append(lg)
        
    return latitude,longitude
    
columns=['date', 'time', 'weekDay', 'latitude', 'longitude', 'temperature', 'power']   
def generateDf(N,u,date,startTime,inter=5,temp=17):
    '''
        N:   total lines of dataset
        u:   the change coefficient of  latitude&longitude
        date: dataset date     #'2020-06-03'
        startTime: start time  #'09:30:00'
        inter: time interval
        temp: temperature
    '''
    
    dates,weekdays,times = genDataTime(N,date,startTime,inter)
    latitude,longitude = genLocation(N,u=u)
    temperature = temp + getRandomTempFromDate(date) + noise(N=N, b= 0.6).round(1)
    power = np.zeros((N,)) + 0.99
    
    df = pd.DataFrame()

    df = pd.concat([df, pd.DataFrame(dates, columns=['date'])], axis=1)
    df = pd.concat([df, pd.DataFrame(times, columns=['time'])], axis=1)
    df = pd.concat([df, pd.DataFrame(weekdays, columns=['weekDay'])], axis=1)
    df = pd.concat([df, pd.DataFrame(latitude, columns=['latitude'])], axis=1)
    df = pd.concat([df, pd.DataFrame(longitude, columns=['longitude'])], axis=1)
    df = pd.concat([df, pd.DataFrame(temperature, columns=['temperature'])], axis=1)
    df = pd.concat([df, pd.DataFrame(power, columns=['power'])], axis=1)

    ##df.set_index(["date"], inplace=True)
    #print('\n\nAfter preprocess:\n',df.head())
    #print('df.shape=', df.shape)
    return df
 
def generateAll(days=60):
    base=r'./db/'
    file = base + 'petIotRecordsAll.csv'
    df = generateData(days=days)
    writeToCsv(df,file)
    
def generateData(startDate='2020-05-01',days=60,everydayLine=250,intersecond=12):
    time = '09:30:00'
    sDate=datetime.datetime.strptime(startDate,'%Y-%m-%d')
    
    df = pd.DataFrame()
    for i in range(days):
        d = sDate + datetime.timedelta(days=i)
        d = datetime.datetime.strftime(d,'%Y-%m-%d')
        
        randomLine = getRandomLenFromDate(d)
        print('d=',d,randomLine)
        
        dfDay = generateDf(N=everydayLine+randomLine,u=0.0001,date=d,startTime='09:30:00',inter=intersecond,temp=18)
        df = df.append(dfDay,ignore_index=True)
    
    df.set_index(["date"], inplace=True)
    return df

def generateOne():
    base=r'./db/'
    file = base + 'petIotRecords.csv'
    df = generateDf(N=100,u=0.003,date='2020-06-03',startTime='09:30:00',inter=5,temp=18)
    #print(df)
    writeToCsv(df,file)
    
def main():
    #generateOne()
    #a = noise(N=100,b=0.005)
    #print(a)
    #getTimeLen('09:30:00','09:32:23')
    generateAll(days=60)#60
    pass
    
if __name__=='__main__':
    main()
    