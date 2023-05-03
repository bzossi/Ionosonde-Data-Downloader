# Ionosonde Data Downloader

Ionosonde Data Downloader uses internet conection to acquire ionospheric data from different repositories, present version contains
* Australia (sws.bom.gov.au)
* Japan (wdc.nict.go.jp)
* GIRO database.

Please check the conditions of data usage for each repository:
* https://sws.bom.gov.au/World_Data_Centre
* https://wdc.nict.go.jp/IONO/HP2009/contact_us_e.html
* https://giro.uml.edu/didbase/RulesOfTheRoad.html

Acknowledge if data is used

This version downloads one complete year of available foF2, hmF2, foE, hmE and M3000F2 (only Australia and GIRO).

Time resolution, missing years and data reliability depends on each repository.

The code was developed and tested on Linux-Ubuntu and Windows 11 (Anaconda), using Python 3.8 (and higher).

This code uses Pandas DataFrame, if not installed try:
```
pip install pandas
or
conda install pandas
```

openxls for Excel output, if not installed:

```
pip install openpyxl
or
conda install openpyxl
```

Simple use with 0-Test.py

From terminal or CMD
```
$ python 0-Test.py 
```
Returns a list to choose 
```
1 - Australian
2 - Japanese
3 - GIRO (Stations from all the world)
          
Select a Database: 
```

Once selected, (ex. 1)
```
0       brisbane
1         camden
2       canberra
3          casey
4          cocos
5         darwin
6          davis
7         hobart
8      learmonth
9      macquarie
10        mawson
11     mundaring
12       norfolk
13         perth
14     salisbury
15     tennantck
16    townsville
17      watheroo

Select Station: 
```
For Townsville
```
Searching available years...

Available years: 

1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960
1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969, 1970
1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980
1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990
1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000
2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010
2011, 2012, 2013, 2014, 2014, 2015, 2016, 2017, 2018, 2019
2020, 2021, 2022, 
 Enter year: 
 ```
And select output file format
```
Select a file format for the output:
    1. CSV
    2. Excel
      
2
Excel file saved as 'output.xlsx'
```

## In your code

From a Python console can be use as 'Console.py', note idd create a Pandas DataFrame

```
import iono_data_downloader as idd

df_aus = idd.ionosondesAustralia()

# Japan search for manual and automatic scaled data
df_jap_manual, df_jap_auto = idd.ionosondesJapan()

df_giro = idd.GIRO()
```

In three repositories can be set the station, year and proxy (if needed).

Ex. (Japan-kokubunji):
```
fof2_manual, fof2_auto = idd.ionosondesJapan(station=3, year=2020, proxy = '10.10.0.31:80')
```



