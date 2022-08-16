import pm25
import numpy as np
import pandas as pd
import os
import georasters as gr
from geopy.distance import geodesic as GD
import xarray

#import data from Tif file and convert to dataframe
popdens = gr.from_file('variables/gpw_v4_population_density_rev11_2020_2pt5_min.tif')
pop_df = popdens.to_pandas()
pop_df = pop_df.rename(columns={"x": "Longitude", "y": "Latitude", "value": "pop_density"})
pop_df = pop_df.set_index(["Latitude", "Longitude"])

#soil data
soil = gr.from_file('variables/so2015v2.tif')
soil_df = soil.to_pandas()
soil_df = soil_df.rename(columns={"x": "Longitude", "y": "Latitude", "value": "soil_taxonomy"})
soil_df = soil_df.set_index(["Latitude", "Longitude"])

#remove unnecessary column and row variables from the dataframe
pop_df.drop(columns=['row', 'col'],inplace=True)
soil_df.drop(columns=['row', 'col'],inplace=True)

#convert pop_df into array.
pop_data = pop_df.to_xarray()

#convert soil_df into array
soil_data = soil_df.to_xarray()

#pm2.5 data inport
pm25_df = pd.read_csv("pm25/AQS_US_PM2520210101_20210131.csv")

#create temporary dataframe for unique lat and long of pm2.5
coord_df = pd.DataFrame(columns=["Longitude", "Latitude", "popdens", "soil_taxonomy"])
coord_df["Longitude"] = pm25_df["Longitude"].unique()
coord_df["Latitude"] = pm25_df["Latitude"].unique()


#populate coord_df with population density
row = 0
for index, row1 in coord_df.iterrows():
    #select population densities closest to the latitude and longitude of pm2.5 data
    pop_temp = pop_data.sel(Longitude = row1["Longitude"], Latitude = row1["Latitude"], method = "nearest").to_array()

    #select soil data closest to latitude and longitude of pm2.5 data
    soil_temp = soil_data.sel(Longitude = row1["Longitude"], Latitude = row1["Latitude"], method = "nearest").to_array()

    #add data to coord_df
    coord_df.at[row, "popdens"] = pop_temp.item(0)
    coord_df.at[row, "soil_taxonomy"] = soil_temp.item(0)
    row = row + 1

#merge coord_df and the pm_25 dataframe
pm25_df = pm25_df.merge(coord_df, how = "right")

#output combined pm25 dataframe to csv
pm25_df.to_csv(os.path.join("combined_dataframe" + '.csv'), index=False)
