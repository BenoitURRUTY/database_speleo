import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt
import folium
import io,sys
from shapely.geometry import Point
from PyQt5 import QtWidgets, QtWebEngineWidgets


# connect to the db
conn=sqlite3.connect('database.db')

c=conn.cursor()
#def map_caves():
# name
name=c.execute("SELECT Nom FROM cave").fetchall()
name = [i[0] for i in name]
# namebis
namebis=c.execute("SELECT Nom_bis FROM cave").fetchall()
namebis = [i[0] for i in name]
# X
X=c.execute("SELECT X FROM cave").fetchall()
results_as_list = [i[0] for i in X]
X = np.fromiter(results_as_list, dtype=np.int32)
# Y
Y=c.execute("SELECT Y FROM cave").fetchall()
results_as_list = [i[0] for i in Y]
Y = np.fromiter(results_as_list, dtype=np.int32)
# ESPG
#EPSG=c.execute("SELECT EPSG FROM cave").fetchall()
#results_as_list = [i[0] for i in ESPG]
#ESPG= np.fromiter(results_as_list, dtype=np.int32)
# geodata
df=pd.DataFrame(data={'X':X,'Y':Y })
gdf = gpd.GeoDataFrame(list(name),crs={'init': 'epsg:27572'},geometry=gpd.points_from_xy(list(df.X),list(df.Y)))
caves_wgs84 = gdf.to_crs({'init': 'epsg:4326'})
test=np.array(caves_wgs84.bounds)
# maps
myMap = folium.Map(location=[45.180772, 5.716572])
for i in range(len(test[:,0])):
    text=str(name[i])#+' \n Autres noms:'+str(df.Nom_bis[i])+'\n Position: \n '+str(test[i,1])+'°E \n'+ str(test[i,0])+'°N \n Altitude='+str(df.Alt[i])+'m denivele='+str(df.denivele[i])+'m \n developpement='+str(df.developpement[i])+'m'
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
#return w.show()
