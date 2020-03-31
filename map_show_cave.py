import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import folium
import io,sys
from shapely.geometry import Point

def get_frame(url,width,height): #https://stackoverflow.com/questions/29535715/python-with-folium-how-can-i-embed-a-webpage-in-the-popup
    html = """ 
        <!doctype html>
    <html>
    <iframe id="myIFrame" width="{}" height="{}" src={}""".format(width,height,url) + """ frameborder="0"></iframe>
    <script type="text/javascript">
    var resizeIFrame = function(event) {
        var loc = document.location;
        if (event.origin != loc.protocol + '//' + loc.host) return;

        var myIFrame = document.getElementById('myIFrame');
        if (myIFrame) {
            myIFrame.style.height = event.data.h + "px";
            myIFrame.style.width  = event.data.w + "px";
        }
    };
    if (window.addEventListener) {
        window.addEventListener("message", resizeIFrame, false);
    } else if (window.attachEvent) {
        window.attachEvent("onmessage", resizeIFrame);
    }
    </script>
    </html>"""

    popup = get_frame(url,
                  width,
                  height)

    marker = folium.CircleMarker([lat,lon],
                             radius=radius,
                             color='#3186cc',
                             fill_color = '#3186cc',
                             popup=popup)

    marker.add_to(map)



    iframe = folium.element.IFrame(html=html,width=width,height=height)
    popup = folium.Popup(iframe,max_width=width)
    return popup

url='./database_speleo_gucem.csv'

data=pd.read_csv(url,sep=';')
FILE_HEADER = ['Nom','Nom_bis','Massif','WGS84','X','Y','Alt','denivele','developpement','Equipement','Temps_approx','debutant','crue','balade']
USE_COLS = FILE_HEADER
 
df = pd.read_csv(
    url, delimiter=";", header=None,
    names=FILE_HEADER, usecols=USE_COLS,skiprows=1)

gdf = gpd.GeoDataFrame(
    df.drop(['X', 'Y'], axis=1),
    crs={'init': 'epsg:27572'},
    geometry=[Point(xy) for xy in zip(df.X, df.Y)])

caves_wgs84 = gdf.to_crs({'init': 'epsg:4326'})

test=np.array(caves_wgs84.bounds)
myMap = folium.Map(location=[45.180772, 5.716572])
for i in range(len(test[:,0])):
    text=str(df.Nom[i])+'\n Autres noms:'+str(df.Nom_bis[i])+'\n'+str(test[i,1])+'°E \n'+ str(test[i,0])+'°N \n Altitude='+str(df.Alt[i])+'m denivele='+str(df.denivele[i])+'m \n developpement='+str(df.developpement[i])+'m'
    folium.Marker([test[i,1],test[i,0]],popup=text).add_to(myMap)


myMap.save('test.html')


from PyQt5 import QtWidgets, QtWebEngineWidgets

app = QtWidgets.QApplication(sys.argv)
    
data = io.BytesIO()
myMap.save(data, close_file=False)

w = QtWebEngineWidgets.QWebEngineView()
w.setHtml(data.getvalue().decode())
w.resize(640, 480)
w.show()

#sys.exit(app.exec_()) #quitte python quand on ferme la fenetre


