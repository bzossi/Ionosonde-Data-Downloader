
# fof2 = GIRO(proxy = '10.10.0.31:80')

def GIRO(station = None, year = None, proxy = None):
    '''
    Return a Pandas DataFrame with:
        CS[confidence] foF2   foE    hmE   hmF2
    
    Data availability depends on GIRO updates, 
    take into account some stations has several data gaps
    
    Time resolution depends on station (from 5 minutes to hour)
    
    Ex:
        df = GIRO()
        print(df)
    '''
    #The simplest way: this routine takes data directly from GIRO's URL
    
    
    from numpy import nan
    from pandas import read_csv, read_table, to_datetime, errors
    from time import sleep
    
    from datetime import date
    #ssl needed to request data from URL
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context
    
    # from urllib.error import HTTPError
    import urllib.request
    
    #define proxy, sometimes doesn't work if not set as None
    proxies = urllib.request.ProxyHandler({'http': proxy})
    if proxy != None:
        proxies = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
    opener  = urllib.request.build_opener(proxies)
    urllib.request.install_opener(opener)
    
    #Take stations list from file
    stats = read_csv('Giro_stats.csv', sep=';')
    
    if station == None:
       stationslist = [f'{i:<2}: {stats.loc[i]["STATION NAME"]:<20}; \
       {i+1:<2}: {stats.loc[i+1]["STATION NAME"]:<20}; \
       {i+2:<2}: {stats.loc[i+2]["STATION NAME"]:<20};\
       {i+3:<2}: {stats.loc[i+2]["STATION NAME"]:<20}' for i in range(0,95,4)]
                       
       for i in stationslist:
           print(i) 
           
       station = int(input('\nSelect one station number (U = updated): '))
        
    code = stats.URSI[station]
    
    if year == None:
        print('Data available:')
        #check if station is updated until present
        today = date.today()
        dd = str(today.day).zfill(2)
        mm = str(today.month).zfill(2)
        yyyy = str(today.year)
        url = f'https://lgdc.uml.edu/common/DIDBGetValues?ursiCode={code}&charName=foF2,foE,hmF2,hmE,MUFD&DMUF=3000&fromDate={yyyy}%2F{mm}%2F{dd}+00%3A00%3A00&toDate={yyyy}%2F{mm}%2F{dd}+23%3A59%3A00'
        df = read_table(url)
    
        t0 = stats.loc[station]["EARLIEST DATA"]
        t1 = stats.loc[station]["LATEST DATA"]
    
        if df.values[-1] != 'ERROR: No data found for requested period':
            t1 = 'Present'
    
        print(f'from {t0}.\nTo {t1} \n')
    

        sleep(0.5) #Sleep to avoid "input" take text printed before =\ (often happens)
        year = input('Select year: ')
    
    print('Downloading (time depends on GIRO servers status and your internet connection, can take secs to mins)')
    
    
    url = f'https://lgdc.uml.edu/common/DIDBGetValues?ursiCode={code}&charName=foF2,foE,hmF2,hmE,MUFD&DMUF=3000&fromDate={year}%2F01%2F01+00%3A00%3A00&toDate={year}%2F12%2F31+23%3A59%3A00'
    
    # print(url)
    
    try:
        df = read_table(url, skiprows=24, delim_whitespace=True)
    except errors.EmptyDataError:
        print('\n\nYear has not data, try again')
        return
    try:
        df.index = to_datetime(df['#Time'].str.slice(stop=-5))
    except KeyError:
        print('\n\nYear has not data, try again')

    df.index.name = 'time'
    
    df = df.drop(columns=['#Time', 'QD', 'QD.1', 'QD.2', 'QD.3', 'QD.4'] )
    
    df = df.replace('---', nan)
    
    df = df.astype('float64')
    
    df.rename(columns={'CS':'Confidence'})
    
    return df, stats['STATION NAME'][station], year

















