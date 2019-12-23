import pandas as pd
from sqlalchemy import create_engine
import sqlite3
import numpy as np

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

# query
NAME=input('nom de la grotte=')

t=c.execute("SELECT * FROM cave where Nom LIKE '%" + NAME + "%'").fetchall()
print(t)

#select all coordinate
X=c.execute("SELECT X FROM cave").fetchall()
Y=c.execute("SELECT Y FROM cave").fetchall()
#EPSG=c.execute("SELECT EPSG FROM cave").fetchall()

### FUNCTION
# query
def search_cave():
    NAME=input('nom de la grotte=')

    t=c.execute("SELECT * FROM cave where Nom LIKE '%" + NAME + "%'").fetchall()
    print(t)
    return


#à faire
def closest(myX,myY,myESPG):
    return name

def add_caves(name,X,Y,ESPG):
    return

def modify_caves(name):
    return

def search():
    return output
