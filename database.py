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

def row_caves(act=1,*var):
    act=str(act)
    if act=='1':
        print('This function is made to add, update or remove a cave in the database \n the function work as row_caves(act,values) \n the argument act can be "add", "update" or "remove" \n add: values is all the values for each columns \n remove: "indexvalue" is the index of the rows \n update: "columnname" is  name of the column "values" is the values to add "indexvalue" is the index of the rows ')
    if act=='add':
        values=var
        c.execute('INSERT INTO cave('+ str(colname) +' ) VALUES( ' + str(values) + ')')
    if act=='remove':
        indexvalue=var
        c.execute('DELETE FROM cave WHERE index =' + str(indexvalue) )
    if act=='update':
        columnname=var[0]
        values=var[1]
        indexvalue=var[2]
        c.execute('UPDATE cave SET' + str(columnname) + '=' + str(values) + 'WHERE index='+ str(indexvalue))


def search():
    return output
