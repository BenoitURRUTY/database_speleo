import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
import io,sys,os
from shapely.geometry import Point
from PyQt5 import QtWidgets, QtWebEngineWidgets

# connect to the db
conn=sqlite3.connect('database.db')

c=conn.cursor()
#colname
colname=c.execute("PRAGMA table_info(cave);").fetchall()
colname = [i[1] for i in colname]
colname = colname [1:]
variablelist=globals()
for i in colname:
    temp=c.execute("SELECT "+ i +" FROM cave").fetchall()
    variablelist[i]=[i[0] for i in temp]

# ESPG
#EPSG=c.execute("SELECT EPSG FROM cave").fetchall()
#results_as_list = [i[0] for i in ESPG]
#ESPG= np.fromiter(results_as_list, dtype=np.int32)

# geodata
df=pd.DataFrame(data={'X':X,'Y':Y })
gdf = gpd.GeoDataFrame(Nom,crs={'init': 'epsg:27572'},geometry=gpd.points_from_xy(list(df.X),list(df.Y)))
caves_wgs84 = gdf.to_crs({'init': 'epsg:4326'})
test=np.array(caves_wgs84.bounds)

# maps
myMap = folium.Map(location=[45.180772, 5.716572])
for i in range(len(Nom)):
    text=str(Nom[i])
    folium.Marker([test[i,1],test[i,0]],popup=text).add_to(myMap)

myMap.save('test.html')
app = QtWidgets.QApplication(sys.argv)
data = io.BytesIO()
myMap.save(data, close_file=False)
w = QtWebEngineWidgets.QWebEngineView()
w.setHtml(data.getvalue().decode())
w.resize(640, 480)
w.show()
sys.exit(app.exec_()) #quitte python quand on ferme la fenetre
