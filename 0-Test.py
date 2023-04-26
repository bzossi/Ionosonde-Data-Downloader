import sys

import numpy as np
from time import sleep

print('''
      
Welcome to Ionospheric Data Downloader.
This code will provide you with an output file (Excel or CSV) with a complete 
year of available data in online repositories

Current version returns foF2, hmF2, foE, hmE, and M3000F2 (Australia and GIRO)

Data time resolution depends on repository

      ''')

sleep(0.5)

# Select Database, loop until selection is valid
while True:
    print('''
1 - Australian
2 - Japanese
3 - GIRO (Stations from all the world)
          ''')
          
    sleep(0.5)
    DB = int(input('Select a Database: '))

    print()
    
    if (DB>3) | (DB<1):
        print('Select a valid Database')
        continue
    else:
        break

def jap():
    from iono_data_downloader import ionosondesJapan
    df_manual, df_auto = ionosondesJapan()
    df_manual = df_manual.replace(np.nan, -1)
    df_auto = df_auto.replace(np.nan, -1)
    return df_manual, df_auto

def aus():
    from iono_data_downloader import ionosondesAustralia
    df = ionosondesAustralia()
    return df

def GIRO():
    from iono_data_downloader import GIRO
    df = GIRO()
    return df


while True:
    if DB==1:
        df = aus()
        try:
            df = df.replace(np.nan, -1)
            break
        except AttributeError:
            continue
    elif DB==2:
        df_manual, df_auto = jap()
        df_manual = df_manual.replace(np.nan, -1)
        df_auto = df_auto.replace(np.nan, -1)
        if (df_manual.shape[0]!=0) | (df_auto.shape[0]!=0):
            break
    elif DB==3:
        df = GIRO()
        try:
            df = df.replace(np.nan, -1)
            break
        except AttributeError:
            continue


print('''
Select a file format for the output:
    1. CSV
    2. Excel
      ''')
choice = int(input())


# Export the DataFrame to the selected file format
if DB !=2:
    if choice == 1:
        df.to_csv('output.csv')
        print("CSV file saved as 'output.csv'")
    elif choice == 2:
        df.to_excel('output.xlsx')
        print("Excel file saved as 'output.xlsx'")
    else:
        print("Invalid choice.")
else:
    print(
        '''
Two files are created, manual and automatic scaled ionograms,
take into account one file could be empty
        ''')
    if choice == 1:
        df_manual.to_csv('output_manual.csv')
        df_auto.to_csv('output_auto.csv')
        print("CSV file saved as 'output.csv'")
    elif choice == 2:
        df_manual.to_excel('output_manual.xlsx')
        df_auto.to_excel  ('output_auto.xlsx')
        print("Excel file saved as 'output.xlsx'")
    else:
        print("Invalid choice.")









