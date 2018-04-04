# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 13:56:35 2018

@author: jesus
"""
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

grafitti = 'https://data.cityofchicago.org/api/views/hec5-y4x5/rows.csv?accessType=DOWNLOAD&api_foundry=true'
vacant = 'https://data.cityofchicago.org/api/views/7nii-7srd/rows.csv?accessType=DOWNLOAD&api_foundry=true'
lights = 'https://data.cityofchicago.org/api/views/t28b-ys7j/rows.csv?accessType=DOWNLOAD&api_foundry=true'

grafitti_df = pd.read_csv(grafitti)
vacant_df = pd.read_csv(vacant)
lights_df = pd.read_csv(lights)

def get_df_year(df, ID, date, y):
    wl = []
    df['d'] = df[date]
    for index, row in df.iterrows():
        if row.d[-4:] == y:
            wl.append([row[ID], y])
    
    int_df = pd.DataFrame(wl, columns = ['id', 'year'])
    int_df = int_df.merge(df, left_on='id', right_on=ID, how='left')
    return int_df
g17 = get_df_year(grafitti_df, 'Service Request Number', 'Creation Date', '2017')
v17 = get_df_year(vacant_df, 'SERVICE REQUEST NUMBER','DATE SERVICE REQUEST WAS RECEIVED', '2017')
l17 = get_df_year(lights_df, 'Service Request Number', 'Creation Date', '2017')

total = len(g17.id.unique()) + len(v17.id.unique()) + len(l17.id.unique())
# Pie chart:
sizes = [len(g17.id.unique())/total * 100 , len(v17.id.unique())/total * 100, len(l17.id.unique())/total * 100]
labels = 'Graffiti Removal', 'Vacant/Abandoned Building', 'Alley Light Out'
explode = (0.1, 0, 0)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
ax1.axis('equal')  

plt.show()

def get_top(df, var, top):
    count_df = df.groupby(var)['id'].count()
    return count_df.nlargest(top)

def notcompleted_rate(df):
    return len(df[(df.Status == 'Open - Dup') | (df.Status == 'Open')])/len(df) * 100

    
    

merged17 = g17.merge(v17, left_on='id', right_on='id', how='outer')
merged17 = merged17.merge(l17, left_on='id', right_on='id', how='outer')


prueba = gpd.read_file('C:/Users/jesus/.spyder-py3/cb_2016_17_bg_500k/cb_2016_17_bg_500k.shp')
blockscc = prueba[prueba.COUNTYFP == '031']

tracts = gpd.read_file('C:/Users/jesus/.spyder-py3/cb_2016_17_tract_500k/cb_2016_17_tract_500k.shp')
tractscc = tracts[tracts.COUNTYFP == '031']

zips = gpd.read_file('C:/Users/jesus/.spyder-py3/cb_2016_us_zcta510_500k/cb_2016_us_zcta510_500k.shp')

blockscc.merge(zips, left_on='AFFGEOID', right_on='AFFGEOID10', how='left') 

bg_list = []
for index_z, poly_z in zc_cc.iterrows():
    for index_b, poly_b in blockscc.iterrows():
        if poly_b.geometry.within(poly_z.geometry) == True:
            poly_b.zip_code == poly_z.ZCTA5CE10

for index_z, poly_z in zc_cc.iterrows():
    for index_b, poly_b in blockscc.iterrows():
        if poly_b.geometry.within(poly_z.grometry) == True:
            bg_list.append([poly_b.TRACTCE, poly_b.BLKGRPCE, poly_b.AFFGEOID, poly_b.GEOID, poly_b.ALAND, poly_z.zip_code, poly_b.geometry])
   
gb_poly = pd.DataFrame(bg_list, columns = ['TRACTCE', 'BLKGRPCE', 'AFFGEOID', 'GEOID', 'ALAND', 'zip_code', 'geometry']) 

bg_list_c = []

for index_z, poly_z in zc_cc.iterrows():
    for index_b, poly_b in blockscc.iterrows():
        if poly_b.geometry.centroid.within(poly_z.grometry) == True:
            bg_list_c.append([poly_b.TRACTCE, poly_b.BLKGRPCE, poly_b.AFFGEOID, poly_b.GEOID, poly_b.ALAND, poly_z.zip_code, poly_b.geometry])
   
gbc_poly = pd.DataFrame(bg_list_c, columns = ['TRACTCE', 'BLKGRPCE', 'AFFGEOID', 'GEOID', 'ALAND', 'zip_code', 'geometry']) 
   

def get_req_points(df, zip_code, lat, lon):
    wlist = []
    df = df.dropna(axis = 0, how = 'all')
    df = df.fillna(0)
    for i, r in df.iterrows():
        wlist.append([r.id, r.year, str(int(r[zip_code])), r[lat], r[lon] ])
        
    intermediate_df = pd.DataFrame(wlist, columns = ['id', 'year', 'zip_code', 'lat', 'lon'])
    intermediate_df = intermediate_df.dropna(axis = 0, how = 'any')
    
    geometry = [Point(xy) for xy in zip(intermediate_df.lon, intermediate_df.lat)]
    intermediate_df = intermediate_df.drop(['lat', 'lon'], axis=1)
#projection used
    crs = {'init': 'epsg:4326'}

# Creating the geodataframe of earthquake damage
    gdf = gpd.GeoDataFrame(intermediate_df, crs=crs, geometry=geometry)
    return gdf
pointsg17 = get_req_points(g17, 'ZIP Code', 'Latitude', 'Longitude')
pointsv17 = get_req_points(v17, 'ZIP CODE', 'LATITUDE', 'LONGITUDE')
pointsl17 = get_req_points(l17, 'ZIP Code', 'Latitude', 'Longitude')

list_of_zc = list(pointsg17.zip_code.unique())


     
def request_in_block(point_gdf, polygon_gdf, zip_codes_list,filename):
    working_list = []
    for element in zip_codes_list:
        df1 = point_gdf[point_gdf.zip_code == element]
        df2 = polygon_gdf[polygon_gdf.zip_code == element]
        for index, point in df1.iterrows():
            for i, polygon in df2.iterrows():
                if point.geometry.within(polygon.geometry) == True:
                    working_list.append([point.id, polygon.TRACTCE, polygon.BLKGRPCE, polygon.GEOID, polygon.zip_code, polygon.geometry])
    
    df = pd.DataFrame(working_list, columns = ['id','TRACTCE', 'BLKGRPCE', 'GEOID', 'zip_code', 'geometry'])
    df_by_blockgroup = df.groupby(['TRACTCE', 'BLKGRPCE', 'GEOID'], sort = False)['id'].count()
    df_by_blockgroup.to_csv(filename)
    return df_by_blockgroup
        
v_by_gb = request_in_block(pointsv17, gbc_poly, list_of_zc)
l_by_gb = request_in_block(pointsl17, gbc_poly, list_of_zc)
v_by_gb.to_csv('C:/Users/jesus/OneDrive/Documentos/GitHub/ml_hw1/v_by_gb.csv')
l_by_gb.to_csv('C:/Users/jesus/OneDrive/Documentos/GitHub/ml_hw1/l_by_gb.csv')

fin_l= pd.read_csv('C:/Users/jesus/OneDrive/Documentos/GitHub/ml_hw1/l_by_gb.csv', names = ['TRACTCE', 'BLKGRPCE', 'GEOID', 'total'])
fin_v= pd.read_csv('C:/Users/jesus/OneDrive/Documentos/GitHub/ml_hw1/v_by_gb.csv', names = ['TRACTCE', 'BLKGRPCE', 'GEOID', 'total'])

fin_v = fin_v.sort_values('total', axis = 0, ascending=False)
fin_l = fin_l.sort_values('total', axis = 0, ascending=False)

#API request

'https://api.census.gov/data/2015/acs5?get=B01003_001E,B01001_001E,B14002_001E,B25010_001E,B25033_001E&for=block%20group:*&in=state:17%20county:031'


#P3
lat = 41.8665840
lon = -87.7156089
pointp3 = Point(lon, lat)

zip60624 = gbc_poly[gbc_poly.zip_code=='60624']

for i, r in zip60624.iterrows():
    if pointp3.within(r.geometry) == True:
        print(r.GEOID)
        
#result 170318430001

fin_l[fin_l.GEOID == 170318430001]
Out[703]: 
      TRACTCE  BLKGRPCE         GEOID  total
1615   843000         1  170318430001     25

fin_v[fin_v.GEOID == 170318430001]
Out[704]: 
     TRACTCE  BLKGRPCE         GEOID  total
659   843000         1  170318430001      3
len(fin_l)
Out[705]: 1961

len(fin_v)
Out[706]: 884

n [708]: (25/1961) * 100
Out[708]: 1.2748597654258031

(3/884) * 100
Out[709]: 0.3393665158371041
