
import iono_data_downloader as idd


# df_aus = idd.ionosondesAustralia(proxy = '10.10.0.31:80')

df_jap_manual, df_jap_auto = idd.ionosondesJapan(proxy = '10.10.0.31:80')

# df_giro = idd.GIRO(proxy = '10.10.0.31:80')


## NO PROXY

# df_aus = idd.ionosondesAustralia()

# df_jap_manual, df_jap_auto = idd.ionosondesJapan()

# df_giro = idd.GIRO()

