
'''
Ionospheric Data Downloader uses internet conection to acquire ionospheric 
data from different repositories, present version contains
Australia: 'sws.bom.gov.au', Japan: 'wdc.nict.go.jp', and GIRO database.

Use:
Australia:
    df = idd.ionosondesAustralia()
Japan:
    df_manual, df_auto = idd.ionosondesJapan()
GIRO:
    df = idd.GIRO()

Optionally, station (number) and year can be set when calling the functions,
proxy can also be added

Ex (Japan-kokubunji):
    fof2_manual, fof2_auto = idd.ionosondesJapan(station=3, year=2020, proxy = '10.10.0.31:80')
  

      '''


from Australia import ionosondesAustralia
from Japan     import ionosondesJapan
from Giro      import GIRO













