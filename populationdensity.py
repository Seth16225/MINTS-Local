import pm25
import numpy as np
import pandas as pd
import os
import georasters as gr

#import data from Tif file and convert to dataframe
popdens = gr.from_file('variables\gpw_v4_population_density_rev11_2020_2pt5_min.tif')
pop_df = popdens.to_pandas()
pop_df = pop_df.rename(columns={"x": "Latitudes", "y": "Longitude", "value": "pop_density"})


#group data in population density by latitude and longitude
lat_list = pop_df["Latitudes"]
lon_list = pop_df["Longitude"]

#truncate values in dataframe to the 6th decimal to match with PM25 data
decimal = 1
pop_df["Latitudes"] = (((pop_df["Latitudes"]*decimal).astype(int).astype(float))/decimal)
pop_df["Longitude"] = (((pop_df["Longitude"]*decimal).astype(int).astype(float))/decimal)

#remove unnecessary column and row variables from the dataframe
pop_df.drop(columns=['row', 'col'],inplace=True)

#collect data from pm25 and truncate decimals from latitude and longitude
decimal = 1
pm25_df = pd.read_csv("pm25/AQS_US_PM2520210101_20210131.csv")
pm25_df["Latitude"] = (((pm25_df["Latitude"]*decimal).astype(int).astype(float))/decimal)
pm25_df["Longitude"] = (((pm25_df["Longitude"]*decimal).astype(int).astype(float))/decimal)
pm25_df.to_csv(os.path.join("outputs",'pm25' + '.csv'))
pop_df.to_csv(os.path.join("outputs",'temp' + '.csv'))


#merge dataframes
combined_df = pd.merge(pm25_df,pop_df)
combined_df.to_csv(os.path.join("outputs",'combined_dataframe' + '.csv'))

print(pm25_df.dtypes)
print(pop_df.dtypes)