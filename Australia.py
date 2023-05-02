


def ionosondesAustralia(station = None, year = None, proxy=None):
    stations_aus = {'brisbane'  :'bri5d',
                    'casey'     :'cascd',
                    'canberra'  :'cbr5d',
                    'cocos'     :'cck5d',
                    'camden'    :'cdn5d',
                    'davis'     :'davis',
                    'darwin'    :'dwn5d',
                    'hobart'    :'hbt5d',
                    'learmonth' :'lea5d',
                    'macquarie' :'maccd',
                    'mawson'    :'mawcd',
                    'norfolk'   :'nlk5d',
                    'niue'      :'nue5d',
                    'perth'     :'per5d',
                    'scott'     :'sct4d',
                    'townsville':'tvl5d'
                    }

    '''
    Return year fof2 dataframe
    
    Before 2014 hourly data,
    Since  2014, depending on instrument 5 or 10 minutes auto-scaled    
    
    '''
    import pandas as pd
    import numpy as np
    from datetime import datetime
    from urllib.error import HTTPError
    from time import sleep
    
    #define proxy, sometimes doesn't work if not set as None
    import urllib.request
    proxies = urllib.request.ProxyHandler({'http': proxy})
    if proxy != None:
        proxies = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
    opener  = urllib.request.build_opener(proxies)
    urllib.request.install_opener(opener)
    

    #Read stations names from file
    stations = pd.read_csv('Aus_stations.csv', header=None)[0]
    
    if station == None:
        print (stations.to_string())
        print()
        sleep(0.5) #Sleep to avoid "input" take text printed before =\ (often happens)
        station = int(input('Select Station: '))
    
    print()
    print('Searching available years...')
    stat = stations[station]
    aux = pd.read_html(f'https://downloads.sws.bom.gov.au/wdc/iondata/au/{stat}/')[0]
    aux = aux.Name[2][:-4]
    
    if year == None:
        years_avail = pd.read_html('https://downloads.sws.bom.gov.au/wdc/iondata/au/{}/{}.00/'.format(stat, aux))[0]
        years_avail = years_avail.Name.dropna()
        years_avail = years_avail.values[1:]
        years_avail = np.array([int(years_avail[i][-5:-3]) for i in range(len(years_avail))])
        
        years_avail[years_avail>15] += 1900
        years_avail[years_avail<15] += 2000
        years_avail                 = np.sort(years_avail)
        
        # Years look for after 2014
        aft2014 = f'https://downloads.sws.bom.gov.au/wdc/wdc_ion_auto/{stations_aus[stat]}/scl/auto/'
        aft2014 = pd.read_html(aft2014, skiprows=2)[0]['Parent Directory'].str.slice(0,-1)[:-1].astype(int).values+2000
        
        years_avail = np.append(years_avail, aft2014)

        print('\nAvailable years: \n')
        for i in range(1,years_avail.shape[0] + 1):
            end = ', '
            if i%10 == 0:
                end ="\n"
            print(years_avail[i-1], end=end)


        year = int(input('\n Enter year: '))
    

    if year < 2014:
        print('Downloading data...')
    elif year>=2014:
        print('Downloading data... Years after 2014 can take a while (time resolution of minutes)')

    #Australia have hourly scaled before 2014 and minutes after
    #Two routines is needed, second part uses threads to speed up
    if year<2014:
        year = str(year)[2:]
        
        if int(year) < 14:
            days = pd.date_range(datetime(2000+int(year), 1, 1 , 0, 0), 
                                       datetime(2000+int(year), 12, 31 , 23, 0), freq='H').to_pydatetime()
        else:
            days = pd.date_range(datetime(1900+int(year), 1, 1 , 0, 0), 
                                       datetime(1900+int(year), 12, 31 , 23, 0), freq='H').to_pydatetime()
        
        #Aus stats bef 2014 have one file each variable
        # foF2
        aux2 = f'{aux}.00/{aux}00.'
        ionourl = f'https://downloads.sws.bom.gov.au/wdc/iondata/au/{stat}/{aux2}{year}.gz'
        # print(ionourl)
        try:
            data = pd.read_csv(ionourl, compression='gzip', header=None)
        except HTTPError:
            print('Year not found, try another')
            return
        
        fof2aux = [int(data[0].values[j][13+i*5:16+i*5])/10 for j in range(len(data)) for i in range(24)]
        
        fof2       = pd.DataFrame(index=days, data={'fof2':fof2aux})
        fof2.index = fof2.index.rename('Time')
        fof2       = fof2.replace(0, np.nan)
        
        
        # hmF2
        aux2 = '{}.04/{}04.'.format(aux,aux)
        ionourl = f'https://downloads.sws.bom.gov.au/wdc/iondata/au/{stat}/{aux2}{year}.gz'
        print(ionourl)
        try:
            data = pd.read_csv(ionourl, compression='gzip', header=None)
            hmF2aux = [int(data[0].values[j][13+i*5:16+i*5]) for j in range(len(data)) for i in range(24)]
            
            hmF2       = pd.DataFrame(index=days, data={'hmF2':hmF2aux})
            hmF2.index = hmF2.index.rename('Time')
            hmF2       = hmF2.replace(0, np.nan)
        except HTTPError:
            print('hmF2 empty')
            hmF2 = np.nan
            
        
            
        # foE
        aux2 = '{}.20/{}20.'.format(aux,aux)
        ionourl = f'https://downloads.sws.bom.gov.au/wdc/iondata/au/{stat}/{aux2}{year}.gz'
        # print(ionourl)
        try:
            data = pd.read_csv(ionourl, compression='gzip', header=None)
            foEaux = [int(data[0].values[j][13+i*5:16+i*5])/100 for j in range(len(data)) for i in range(24)]
            
            foE       = pd.DataFrame(index=days, data={'foE':foEaux})
            foE.index = foE.index.rename('Time')
            foE       = foE.replace(0, np.nan)
        except HTTPError:
            print('foE empty')
            foE = np.nan
            
           
        # hmE
        aux2 = '{}.24/{}24.'.format(aux,aux)
        ionourl = f'https://downloads.sws.bom.gov.au/wdc/iondata/au/{stat}/{aux2}{year}.gz'
        # print(ionourl)
        try:
            data = pd.read_csv(ionourl, compression='gzip', header=None)
            hmEaux = [int(data[0].values[j][13+i*5:16+i*5]) for j in range(len(data)) for i in range(24)]
            
            hmE       = pd.DataFrame(index=days, data={'hmE':hmEaux})
            hmE.index = hmE.index.rename('Time')
            hmE       = hmE.replace(0, np.nan)
        except HTTPError:
            print('hmE empty')
            hmE = np.nan

        # M3000F2
        aux2 = '{}.07/{}07.'.format(aux,aux)
        ionourl = f'https://downloads.sws.bom.gov.au/wdc/iondata/au/{stat}/{aux2}{year}.gz'
        # print(ionourl)
        try:
            data = pd.read_csv(ionourl, compression='gzip', header=None)
            M3000F2aux = [int(data[0].values[j][13+i*5:16+i*5]) for j in range(len(data)) for i in range(24)]
            
            M3000F2       = pd.DataFrame(index=days, data={'M3000F2':M3000F2aux})
            M3000F2.index = M3000F2.index.rename('Time')
            M3000F2       = M3000F2.replace(0, np.nan)
        except HTTPError:
            print('M3000F2 empty')
            M3000F2 = np.nan
            
        
        fof2['hmF2'] = hmF2
        fof2['foE']  = foE
        fof2['hmE']  = hmE
        fof2['M3000F2']  = M3000F2/100
        
    else: # Year > 2014
        fof2 = aus_2014(year, stat, proxy)
    return fof2, list(stations_aus)[station], year





'''
Australia SINCE 2014
'''

import pandas as pd
from datetime import datetime

def aus_2014(YYYY, stat, proxy=None):
    #define proxy, sometimes doesn't work if not set as None

    stations_aus = {'brisbane'  :'bri5f',
                    'casey'     :'cascf',
                    'canberra'  :'cbr5f',
                    'cocos'     :'cck5f',
                    'camden'    :'cdn5f',
                    'davis'     :'davis',
                    'darwin'    :'dwn5f',
                    'hobart'    :'hbt5d',
                    'learmonth' :'lea5f',
                    'macquarie' :'maccd',
                    'mawson'    :'mawcd',
                    'norfolk'   :'nlk5f',
                    'niue'      :'nue5f',
                    'perth'     :'per5f',
                    'scott'     :'sct4d',
                    'townsville':'tvl5f'
                    }

    import urllib.request
    proxies = urllib.request.ProxyHandler({'http': proxy})
    if proxy != None:
        proxies = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
    opener  = urllib.request.build_opener(proxies)
    urllib.request.install_opener(opener)

    from urllib.error import HTTPError
    #Separa el codigo de la estacion
    station = stations_aus[stat]
    
    #rango de dias, esta parte esta por dia
    start_date = datetime(YYYY, 1, 1)
    end_date   = datetime(YYYY, 5, 31)
    dates = pd.date_range(start_date, end_date, freq='D').to_pydatetime()

    #Search for data, if not, change instrument, basically 'd' for 'f' the last, for townsville can be tvl5d ,5f,6a,cd
    for a in ['5d', '6a', 'cd']:
        url = f'https://downloads.sws.bom.gov.au/wdc/wdc_ion_auto/{station}/scl/auto/{str(YYYY)[-2:]}/'
        # print(url)
        try:
            aux = pd.read_html(url)[0].Name.dropna()[1:].values
        except HTTPError:
            station = station[:-2] + a
            continue
        # I think this 'if' is not necessary
        if aux.shape[0]<10:
            station = station[:-2] + a
            continue
        else:
            break

    avail_day_files = [url + aux[i] for i in range(len(aux))]

    from joblib import Parallel, delayed
    auxfof2 = Parallel(n_jobs=20, backend='threading')(delayed(aus)(urls, proxy = proxy) for urls in avail_day_files)

    # auxfof2 = [aus(urls, proxy = proxy) for urls in avail_day_files]

    fof2 = pd.DataFrame()
    for i in range(len(auxfof2)):
        fof2 = pd.concat([fof2, auxfof2[i]])

    
    #if year is not complete, change stations instrument
    if len(avail_day_files)<200:
        # print(f'Time resolution could change since {pd.to_datetime("20"+aux[-1][:-4])}')
        station = station[:-2] + '5f'
        url = f'https://downloads.sws.bom.gov.au/wdc/wdc_ion_auto/{station}/scl/auto/{str(YYYY)[-2:]}/'
        try:
            aux = pd.read_html(url)[0].Name.dropna()[1:].values
        except HTTPError:
            return
        
        avail_day_files = [url + aux[i] for i in range(len(aux))]

        from joblib import Parallel, delayed
        auxfof2 = Parallel(n_jobs=20, backend='threading')(delayed(aus)(urls, proxy = proxy) for urls in avail_day_files)

        # auxfof2 = [aus(urls, proxy = proxy) for urls in avail_day_files]

        for i in range(len(auxfof2)):
            fof2 = pd.concat([fof2, auxfof2[i]])

    return fof2 


def aus(url, proxy=None):
    import numpy as np
    from urllib.error import HTTPError
    import urllib.request
    import pandas as pd
    
    proxies = urllib.request.ProxyHandler({'http': proxy})
    if proxy != None:
        proxies = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
    opener  = urllib.request.build_opener(proxies)
    urllib.request.install_opener(opener)

    # print (url)
    try:
        daily = pd.read_csv(url, header=None)
    except HTTPError:
        return
    f2   = daily[0].str.slice(-25, -22).astype('int64')/10
    hmf2 = daily[0].str.slice(-15, -12).astype('int64')
    foE  = daily[0].str.slice(16, 19).astype('int64')/100
    hmE  = daily[0].str.slice(21, 24).astype('int64')
    M3000F2  = daily[0].str.slice(-5, -2).astype('int64')/100
    # add year, can be done directly from str method....
    time  = pd.to_datetime(daily[0].str.slice(stop = 10).astype('int64')+200000000000, format='%Y%m%d%H%M')
    
    fof2day = pd.DataFrame(data={'fof2': f2, 
                                 'hmf2': hmf2, 
                                 'foE': foE, 
                                 'hmE': hmE,
                                 'M3000F2': M3000F2})

    fof2day.index = time; fof2day.index.name = 'time'
    # zero to nan
    fof2day= fof2day.replace(0, np.nan)
    return fof2day






