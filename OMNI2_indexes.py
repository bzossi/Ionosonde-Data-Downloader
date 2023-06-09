

# Check internet connection 
def connect(proxy=None):
    import urllib.request
    try:
        urllib.request.urlopen('http://google.com') #Python 3.x
        return True
    except:
        return False


# Download OMNI 2 indexes and SW conditions hourly
def OMNI2_indexes(year = None, proxy = None):
    '''
    Returns Pandas DataFrame with following variables:
        'Bartels number', 'ID IMF spacecraft', 'ID SW spacecraft', 
        'n points IMF averages', 'n points plasma averages', 
        'Field Magnitude Average', 'Magnitude Average Field Vector', 
        'Lat.Angle Aver. Field Vector','Long.Angle Aver.Field Vector', 
        'Bx', 'ByGSE', 'BzGSE', 'ByGSM', 'BzGSM', 
        'sigma|B|', 'sigma B', 'sigma Bx', 'sigma By', 'sigma Bz',
        'Proton temp', 'Proton Dens', 'Plasma speed', 'Plasma Long. Angle', 
        'Plasma Lat. Angle', 'Alpha/Proton ratio', 'Flow Pressure',
        'sigma T', 'sigma N', 'sigma V', 'sigma phi V', 'sigma theta V', 
        'sigma-Alpha/Proton', 'Electric field', 'Plasma beta', 'Alfven mach number',
        'Kp', 'R', 'dst', 'AE-index', 'Proton flux >1 Mev', 
        'Proton flux >2 Mev', 'Proton flux >4 Mev', 'Proton flux >10 Mev', 
        'Proton flux >30 Mev','Proton flux >60 Mev', 'Flag', 'ap-index', 
        'f10.7_index', 'PC(N) index', 'AL-index', 'AU-index', 
        'Mach number'

    Check OMNI2 description for more info:
    https://spdf.gsfc.nasa.gov/pub/data/omni/low_res_omni/omni2.text
    '''
    
    import pandas as pd
    import urllib.request

    #define proxy, sometimes doesn't work if not set as None
    proxies = urllib.request.ProxyHandler({'http': proxy})
    if proxy != None:
        proxies = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
    opener  = urllib.request.build_opener(proxies)
    urllib.request.install_opener(opener)

    # Omni2 all variables indexes
    url = f"https://spdf.gsfc.nasa.gov/pub/data/omni/low_res_omni/omni2_{year}.dat"
    
    OMNI2_Variables = ['year', 'DOY', 'hour', 'Bartels', 'ID IMF spacecraft', 'ID SW spacecraft', 
                       'n points IMF averages', 'n points plasma averages', 
                       'Field Magnitude Average', 'Magnitude Average Field Vector', 
                       'Lat.Angle Aver. Field Vector','Long.Angle Aver.Field Vector', 
                       'Bx', 'ByGSE', 'BzGSE', 'ByGSM', 'BzGSM', 
                       'sigma|B|', 'sigma B', 'sigma Bx', 'sigma By', 'sigma Bz',
                       'Proton temp', 'Proton Dens', 'Plasma speed', 'Plasma Long. Angle', 
                       'Plasma Lat. Angle', 'Alpha/Proton ratio', 'Flow Pressure',
                       'sigma T', 'sigma N', 'sigma V', 'sigma phi V', 'sigma theta V', 
                       'sigma-Alpha/Proton', 'Electric field', 'Plasma beta', 'Alfven mach number',
                       'Kp', 'R', 'dst', 'AE-index', 'Proton flux >1 Mev', 
                       'Proton flux >2 Mev', 'Proton flux >4 Mev', 'Proton flux >10 Mev', 
                       'Proton flux >30 Mev','Proton flux >60 Mev', 'Flag', 'ap-index', 
                       'f10.7_index', 'PC(N) index', 'AL-index', 'AU-index', 
                       'Mach number'
                       ]
    df = pd.read_table(url, delim_whitespace=True, header = None,  names = OMNI2_Variables)

    df.index = pd.to_datetime(df['year'] * 100000 + 
                              df['DOY']*100 + 
                              df['hour'], format='%Y%j%H')
    df = df.drop(columns=['year','DOY','hour'])
    
    return df







'''
Kyoto dst (monthly, missing current month recognition of 9999)
'''

# def dst_download(year = None, month = None, proxy = None):
    
#     import pandas as pd
#     import urllib.request

#     #define proxy, sometimes doesn't work if not set as None
#     proxies = urllib.request.ProxyHandler({'http': proxy})
#     if proxy != None:
#         proxies = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
#     opener  = urllib.request.build_opener(proxies)
#     urllib.request.install_opener(opener)
    
#     # Date in str format for url
#     date = f'{year}{str(month).zfill(2)}'
#     url = f'https://wdc.kugi.kyoto-u.ac.jp/dst_final/{date}/index.html'
    
#     df = pd.read_table(url, header = 28, names=["hh"]).drop([0])
    
#     # Last row have this text
#     end = '<!-- vvvvv S yyyymm_part3.html vvvvv -->'
#     last_data = df[df==end].dropna().index[0]
    
#     # df until last data
#     df = df.loc[:last_data-1]
    
#     # Remove day column, separating text in columns
#     df = df['hh'].str.slice(3).str.split(" +",expand = True)
    
#     # drop empty column 0 and change names
#     df = df.drop(columns=0)
#     df.columns = pd.RangeIndex(0,24)
    
#     # Str to integer
#     df = df.astype('int')
    
#     dst_mon = df.values.flatten()
    
#     date = pd.date_range(f'2000-01-01', '2000-02-01', freq='h')[:-1]
    
#     dst = pd.DataFrame(data = {'dst':dst_mon}, index = date)
        

#     return dst









