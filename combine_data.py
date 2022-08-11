import pm25
import numpy as np
import pandas as pd
import os
import georasters as gr
from geopy.distance import as dst

#import data from Tif file and convert to dataframe
popdens = gr.from_file('variables\gpw_v4_population_density_rev11_2020_2pt5_min.tif')
pop_df = popdens.to_pandas()
pop_df = pop_df.rename(columns={"x": "Longitude", "y": "Latitude", "value": "pop_density"})

#remove unnecessary column and row variables from the dataframe
pop_df.drop(columns=['row', 'col'],inplace=True)

#convert pop_df into array.
pop_ar = pop_df.to_numpy()
pop_ar = np.delete(pop_ar, 0, axis=1)

#pm2.5 data inport
pm25_df = pd.read_csv("pm25/AQS_US_PM2520210101_20210131.csv")



#creates a longitude and latitude dataframe, then gets unique coordinate pair values from pm25, then associates it with data.
coord_list = pd.DataFrame(columns=["Longitude", "Latitude"])

coord_list["Longitude"] = pm25_df["Longitude"].unique()
coord_list["Latitude"] = pm25_df["Latitude"].unique()


for index, row in coord_list.iterrows():
    distance = dst()
    for row in pop_ar:
        coord_distance = dst(row["Latitude"], row["Longitude"])

        if(distance >= dst(row, ))
        distance = dst(row)
       
    
    



#combined_df = pd.merge(pm25_df,pop_df)
#combined_df.to_csv(os.path.join("outputs",'combined_dataframe' + '.csv'))