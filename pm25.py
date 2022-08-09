
import requests
import pandas as pd
import os
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from cartopy.feature import ShapelyFeature
from cartopy.io.shapereader import Reader

statelist = ['01','04','05','06','07','08','09','10','11','12','13','16','17','18','19','20',
'21','22','23','24','25','26','27','28','29','30','31','32','33','34','35','36','37','38','39',
'40','41','42','44','45','46','47','48','49','50','51','53','54','55','56']

bedate = 20210101
edate=20210131


if not os.path.isfile('pm25/AQS_US_PM2520210101_20210131.csv'):
    concat_df = pd.DataFrame()
    for state in statelist:
        print("Downloading state"+ ' ' + state )
        r = requests.get('https://aqs.epa.gov/data/api/sampleData/byState?email=sethlee2024@gmail.com&key=copperwren85&param=88101&bdate=' + str(bedate) + '&edate=' + str(edate) + '&state='+state)
        try:
            j=r.json()
            print(state + ' ' + 'Download Complete')
            j = j['Data']
            raw_df = pd.DataFrame.from_dict(j)
            AQS_df = pd.DataFrame(raw_df,columns=['latitude','longitude','date_gmt','time_gmt','units_of_measure','sample_measurement'])
            AQS_df["UTC"] = AQS_df['date_gmt'] +"T"+AQS_df['time_gmt']
            AQS_df.rename({'latitude':'Latitude', 'longitude':'Longitude', 'sample_measurement':'Value'}, axis=1,inplace=True)
            AQS_df.drop(columns=['date_gmt','time_gmt','units_of_measure'],inplace=True)
            if concat_df.empty:
                concat_df = AQS_df
            else:
                concat_df = pd.concat([concat_df,AQS_df])
        except:
            print(state + ' ' + 'Failed')
    # Merge states together
    concat_df.to_csv(os.path.join("pm25",'AQS_US_PM25' + str(bedate) + '_' + str(edate) + '.csv'), index=False)














    #df = pd.read_csv("pm25/AQS_US_PM2520210101_20210131.csv")

    # Group data by unique coordinates pairs
    #group_df = df.groupby(["Latitude","Longitude"],as_index=False).count()
    #lat_list = group_df["Latitude"]
    #lon_list = group_df["Longitude"]

'''
# Plot monitoring sites
fig = plt.figure(figsize=[20,13])
ax = fig.add_subplot(
                     projection=ccrs.PlateCarree())
ax.scatter(lon_list, lat_list)
fname = 'US_Boundary/USBoundary.shp'
shape_feature = ShapelyFeature(Reader(fname).geometries(),
                                ccrs.PlateCarree(), facecolor='none')
ax.add_feature(shape_feature,edgecolor='blue')
ax.gridlines(draw_labels=True)
ax.coastlines()

'''