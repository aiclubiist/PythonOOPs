import pandas as pd
sat_data = pd.read_json('satelliteData.json')
print(sat_data.head())

sat_data.to_csv('satelliteData.csv', index=False)
# sat_data.to_sql('satellite_table', 'sqlite:///satelliteData.db', if_exists='replace', index=False)

df_to_insert = sat_data.drop(columns=['telemetries', 'associated_satellites'])
df_to_insert.to_sql('satellite_table', 'sqlite:///satelliteData.db', if_exists='replace', index=False)