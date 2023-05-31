

def ionosondesJapan(station=None, year=None, proxy=None):
    '''
    Return: 
    two Pandas Dataframes 
    fof2 [manually, automatically] scaled.
    Note MANUAL data is hourly spaced while AUTO is 10 or 15-min
    
    Ex:
        fof2_manual, fof2_auto = ionosondesJapan()
    
    If station and/or year is set, skips selection, usefull for looping
    1-Wakkanai, 2-Akita, 3-Kokubunji, 4-Yamagawa, 5-Okinawa
    
    Ex:
        Wakkanai and year 1999
        fof2_manual, fof2_auto = ionosondesJapan(1, 1999) (or station = 1, year = 1999)
    '''
    import pandas as pd
    import numpy as np
    from urllib.error import HTTPError
    import urllib.request
    from time import sleep
    
    #define proxy, sometimes doesn't work if not set as None
    proxies = urllib.request.ProxyHandler({'http': proxy})
    if proxy != None:
        proxies = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
    opener  = urllib.request.build_opener(proxies)
    urllib.request.install_opener(opener)
    
    # define empty DataFrame to avoid error at return None
    manu, auto = pd.DataFrame(), pd.DataFrame()
    
    stations = ['Wakkanai', 'Akita', 'Kokubunji', 'Yamagawa', 'Okinawa']
    
    if station == None:
        print ('''
1) Wakkanai (1948-2023)
2) Akita (1965-1993)
3) Kokubunji (1957-2023)
4) Yamagawa (1965-2023)
5) Okinawa (1972-2023)
               ''')
        sleep(0.5)
        station = int(input('Enter Station: '))
        
    if type(station) is not int:
        print('Station is an integer value')
        return
    
    #Change the selection to stations code
    if station==1: stat = 'WK545'
    if station==2: stat = 'AK539'
    if station==3: stat = 'TO535'
    if station==4: stat = 'YG431'
    if station==5: stat = 'OK426'
        
    if year == None:
        year = int(input( 'Enter year: '))
    # Change station instrument 
    if station==1 and year>2000: stat = 'WK546'
    if station==3 and year>2000: stat = 'TO536'
    
    if type(year) is not int:
        print('Year is an integer value')
        return

    #Manually scaled
    ionourl = f'https://wdc.nict.go.jp/IONO/observation-history/factor-manual-{stat}-{year}H.sjis.txt'
    print(ionourl)
    print('Downloading data...')
    
    try:
        data = pd.read_csv(ionourl)
        data = data.drop(data[data.index=='#                    fmin '].index)

        dates = data[data.keys()[0]].str.slice(start = 0, stop = 14).replace(r'^\s*$', np.nan, regex=True).dropna()
        dates = pd.to_datetime(dates, format='%Y%m%d%H%M%S')
        #Data, the r'^\s*$' means white spaces, there are simpler ways but works
        fof2 = data['foF2 '].str.slice(stop=3).replace(r'^\s*$', np.nan, regex=True).astype('float64')/10
        foE  = data['foE  '].str.slice(stop=3).replace(r'^\s*$', np.nan, regex=True).astype('float64')/100
        hmF2 = data["h'F2 "].str.slice(stop=3).replace(r'^\s*$', np.nan, regex=True).astype('float64')
        hmE  = data["h'E  "].str.slice(stop=3).replace(r'^\s*$', np.nan, regex=True).astype('float64')
        
        # M3000F2  = data["M3F2 "].str.slice(stop=3).replace(r'^\s*$', np.nan, regex=True).astype('float64')/100
        
        manu = pd.DataFrame(data  = {'fof2': fof2,
                                     'foE' : foE, 
                                     'hmE' : hmE, 
                                     'hmF2': hmF2,
                                     # 'M3000F2': M3000F2
                                     })
        manu.index = dates
        manu.index.name = 'time'
        
    except HTTPError:
        print('no data Manually scaled data')


    #Automatically scaled
    ionourl = f'https://wdc.nict.go.jp/IONO/observation-history/factor-auto-{stat}-{year}.sjis.txt'
    print(ionourl)

    try:
        data = pd.read_csv(ionourl)
        data = data.drop(data[data.index == data.keys()[0]].index)
        
        dates = pd.to_datetime(data[data.keys()[0]].str.slice(stop=14), format='%Y%m%d%H%M%S')
        
        fof2 = data['   foF2  '].str.slice(1, 5).replace(r'^\s*$', np.nan, regex=True).astype('float64')/100
        foE = data["   foE   "].str.slice(1, 5).replace(r'^\s*$', np.nan, regex=True).astype('float64')/100
        hmF2 = data["   h'F2  "].str.slice(1, 5).replace(r'^\s*$', np.nan, regex=True).astype('float64')/10
        hmE = data["   h'E   "].str.slice(1, 5).replace(r'^\s*$', np.nan, regex=True).astype('float64')/10
        
        # M3000F2  = data['   M3F2  '].str.slice(stop=3).replace(r'^\s*$', np.nan, regex=True).astype('float64')/100
        #Data
        
        auto = pd.DataFrame(data  = {'fof2': fof2,
                                     'foE' : foE, 
                                     'hmE' : hmE, 
                                     'hmF2': hmF2,
                                     # 'M3000F2': M3000F2
                                     })
        auto.index = dates
        auto.index.name = 'time'
    except HTTPError:
        print('no data automatically scaled data')
        
    
    return manu, auto, stations[station], year



