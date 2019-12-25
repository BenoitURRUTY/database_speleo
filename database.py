import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import numpy as np
import geopandas as gpd

# convert csv to db

def convert_csv_db(pathcsv,pathdb):
    engine = create_engine('sqlite:///'+pathdb, echo=False)
    file=pathcsv
    FILE_HEADER = ['Nom','Nom_bis','Massif','WGS84','X','Y','Alt','denivele','developpement','Equipement','Temps_approx','debutant','crue','balade']
    USE_COLS = FILE_HEADER
    df = pd.read_csv(
        file, delimiter=";", header=None,
        names=FILE_HEADER, usecols=USE_COLS)
    df.to_sql('cave',con=engine)
    return

# connect to the db
conn=sqlite3.connect('database.db')

c=conn.cursor()
#colname
colname=c.execute("PRAGMA table_info(cave);").fetchall()
colname = [i[1] for i in colname]
#colname = colname [1:]


# query
NAME=input('nom de la grotte=')

t=c.execute("SELECT * FROM cave where Nom LIKE '%" + NAME + "%'").fetchall()


#select all coordinate
X=c.execute("SELECT X FROM cave").fetchall()
Y=c.execute("SELECT Y FROM cave").fetchall()
#EPSG=c.execute("SELECT EPSG FROM cave").fetchall()

### FUNCTION

#à faire
def closest(myX,myY,myESPG): #sort data by the distance from my position
    df=pd.DataFrame(data={'X':myX,'Y':myY })
    gdf = gpd.GeoDataFrame(Nom,crs={'init': 'epsg:' + str(myESPG) },geometry=gpd.points_from_xy(list(df.X),list(df.Y)))
    caves_wgs84 = gdf.to_crs({'init': 'epsg:27572'})
    test=np.array(caves_wgs84.bounds)
    dist_X=X-test[:,1]
    dist_Y=Y_test[:,0]
    dist=np.sqrt(dist_X**2+dist_Y**2)
    
    return name

print('This function is made to add, update or remove a cave in the database \n the function work as row_caves(act,values) \n the argument act can be "add", "update" or "remove" \n add: values is all the values for each columns \n remove: "indexvalue" is the index of the rows \n update: "columnname" is  name of the column "values" is the values to add "indexvalue" is the index of the rows ')
def add_row(): # reperer les doublons
    c.execute("INSERT INTO cave DEFAULT VALUES") #create a new empty row
    c.execute("UPDATE cave SET idCave ='" + str(c.lastrowid-1) + "' WHERE idCave IS  NULL")
    for columnname in colname:
        values=input(columnname + ': value of the cell=')
        if values=='':
            values=0
        indexvalue=c.lastrowid-1
        update_row(columnname,values,indexvalue)
    conn.commit()


    
def remove_row(indexvalue):
    c.execute("DELETE FROM cave WHERE idcave =" + str(indexvalue) )
    conn.commit()


def update_row(columnname,values,indexvalue):
    print(indexvalue)
    print(columnname)
    order="UPDATE cave SET " + str(columnname) + " ='" + str(values) + "' WHERE idCave = "+ str(indexvalue)
    print(order)
    c.execute(order)
    z=c.execute("select * from cave where idcave =" + str(indexvalue)).fetchall()
    c.execute("COMMIT")
    print(z)

    
def search(): #found caves by searching
    
    word=input('name of the cave=')
    c.execute("SELECT * FROM cave WHERE Nom,Nom_bis  MATCH '" + str(word) + "' ORDER BY Nom ASC").fetchall()
    

