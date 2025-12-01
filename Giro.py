
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
    
    from datetime import date, timedelta
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
        # Print stations in 4 columns
       stationslist = [f'{i:<2}: {stats.loc[i]["STATION NAME"]:<20}; \
       {i+1:<2}: {stats.loc[i+1]["STATION NAME"]:<20}; \
       {i+2:<2}: {stats.loc[i+2]["STATION NAME"]:<20};\
       {i+3:<2}: {stats.loc[i+2]["STATION NAME"]:<20}' for i in range(0,96,4)]
       
       print()
       for i in stationslist:
           print(i)
       #Last stations
       print(f'95: {stats.loc[95]["STATION NAME"]}               ;',end='')
       print(f'        96: {stats.loc[96]["STATION NAME"]}             ;',end='')
       print(f'        97: {stats.loc[97]["STATION NAME"]}',end='')
       
 
       print()
       station = int(input('\nSelect one station number (U = updated): '))
        
    code = stats.URSI[station]
    
    if year == None:
        print('Data available:')
        # check if station is updated until last two days
        today = date.today()
        dd1 = str(today.day).zfill(2)
        mm1 = str(today.month).zfill(2)
        yyyy1 = str(today.year)
        
        dd0 = str((today - timedelta(2)).day).zfill(2)
        mm0 = str((today - timedelta(2)).month).zfill(2)
        yyyy0 = str((today - timedelta(2)).year)
        url = f'https://lgdc.uml.edu/common/DIDBGetValues?ursiCode={code}&charName=foF2,foE,hmF2,hmE,MUFD&DMUF=3000&fromDate={yyyy0}%2F{mm0}%2F{dd0}+00%3A00%3A00&toDate={yyyy1}%2F{mm1}%2F{dd1}+23%3A59%3A00'
        df = read_table(url)
    
        t0 = stats.loc[station]["EARLIEST DATA"]
        t1 = stats.loc[station]["LATEST DATA"]
        
        
        if df.values[-1] != 'ERROR: No data found for requested period':
            t1 = 'Present'
    
        print(f'from {t0}.\nTo {t1} \n')
        
        print('Some stations could have missing years')

        sleep(0.5) #Sleep to avoid "input" take text printed before =\ (often happens)
        year = input('Select year: ')
    
    print('Downloading (time depends on GIRO servers status and internet connection, can take secs to mins)')
    
    
    url = f'https://lgdc.uml.edu/common/DIDBGetValues?ursiCode={code}&charName=foF2,foF1,foE,foEs,fbEs,foEa,foP,fxI,MUFD,MD,hF2,hF,hE,hEs,hEa,hP,TypeEs,hmF2,hmF1,hmE,zhalfNm,yF2,yF1,yE,scaleF2,B0,B1,D1,TEC,FF,FE,QF,QE,fmin,fminF,fminE,fminEs,foF2p&DMUF=3000&fromDate={year}%2F01%2F01+00%3A00%3A00&toDate={year}%2F12%2F31+23%3A59%3A00'
    
    # print(url)
    
    try:
        df = read_table(url, skiprows=57, sep='\\s+')
    except errors.EmptyDataError:
        print('\n\nYear has not data, try again')
        return
    try:
        df.index = to_datetime(df['#Time'].str.slice(stop=-5))
    except KeyError:
        print('\n\nYear has not data, try again')

    df.index.name = 'time'
    
    df = df.drop(columns=['#Time', 'QD'])
    lastqd = int(df.columns[-1][-2:])+1
    df = df.drop(columns=[f'QD.{i}' for i in range(1, lastqd)])
    
    df = df.replace('---', nan).infer_objects(copy=False)
    
    df = df.astype('float64')
    
    # df.rename(columns={'CS':'Confidence'})
    
    return df, stats['STATION NAME'][station], year

'''
# CS is Autoscaling Confidence Score (from 0 to 100, 999 if manual scaling, -1 if unknown)
# foF2 [MHz] - F2 layer critical frequency
# foF1 [MHz] - F1 layer critical frequency
# MUFD [MHz] - Maximum usable frequency for ground distance D
# fmin [MHz] - Minimum frequency of ionogram echoes
# foEs [MHz] - Es layer critical frequency
# fminF [MHz] - Minimum frequency of F-layer echoes
# fminE [MHz] - Minimum frequency of E-layer echoes
# foE [MHz] - E layer critical frequency
# fxI [MHz] - Maximum frequency of F trace
# FF [MHz] - Frequence spread between fxF2 and fxI
# FE [MHz] - Frequence spread beyond foE
# foF2p [MHz] - Predicted value of foF2
# fminEs [MHz] - Minimum frequency of Es-layer
# foEa [MHz] - Critical frequency of auroral E-layer
# foP [MHz] - Highest ordinary wave critical frequency of F region patch trace
# fbEs [MHz] - Blanketing frequency of Es-layer
# hF [km] - Minimum virtual height of F trace
# hF2 [km] - Minimum virtual height of F2 trace
# hE [km] - Minimum virtual height of E trace
# hEs [km] - Minimum virtual height of Es trace
# hmE [km] - Peak height of E-layer
# yE [km] - Half thickness of E-layer
# QF [km] - Average range spread of F-layer
# QE [km] - Average range spread of E-layer
# hmF2 [km] - Peak height F2-layer
# hmF1 [km] - Peak height F1-layer
# zhalfNm [km] - The true height at half the maximum density in the F2-layer
# yF2 [km] - Half thickness of F2-layer, parabolic model
# yF1 [km] - Half thickness of F1-layer, parabolic model
# scaleF2 [km] - Scale hieght at the F2-peak
# B0 [km] - IRI thickness parameter
# hEa [km] - Minimum virtual height of auroral E-layer trace
# hP [km] - Minimum virtual height of the trace used to determinate foP
# TEC [10^16 m^-2] - Total electron content
# MD [] - MUF(D)/foF2
# B1 [] - IRI profile shape parameter
# D1 [] - IRI profile shape parameter, F1-layer
# TypeEs [] - Type Es
# Distance D for MUF calculations: 3000 km
'''














