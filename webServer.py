"""
    AD - Trabalho 03 - webServer.py
    Manuel Barral 56943, Lilia Colisnyc xxxxx

"""
from flask import Flask, request, make_response
import sqlite3
from os.path import isfile

app = Flask(__name__)

def connectDB(dbname):
    dbIsCreated = isfile(dbname)
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    if not dbIsCreated:
        cursor.execute("PRAGMA foreign_keys = ON;") # Allow foreign keys
        cursor.execute("CREATE TABLE weather (id INTEGER PRIMARY KEY, date INTEGER, location TEXT,\
                        condition TEXT, mintemp_c INTEGER, maxtemp_c INTEGER);") # Create table weather
        cursor.execute("CREATE TABLE locations (id INTEGER, name TEXT, IATA TEXT, wea_name TEXT);") # Criação da tabela locations 
        cursor.execute("CREATE TABLE legs (id TEXT, dep_IATA TEXT, arr_IATA TEXT, dep_datetime INTEGER, arr_datetime INTEGER,\
                        duration_min INTEGER, arlineCodes TEXT)") # Criação da tabela legs (voos)
        cursor.execute("CREATE TABLE roundtrips (id INTEGER, cost INTEGER, id_leg0 TEXT, id_leg1 TEXT)") # Criação da tabela 
        cursor.execute("CREATE TABLE airlines (code TEXT, name TEXT)")
        return connection, cursor
        
connectDB("flightsDB.db")
        
@app.route('/search', methods=["GET"])
def search ():
    pass 

@app.route('/filter', methods= ['GET'])
def filter ():
    pass

@app.route('/details', methods=['GET'])
def details ():
    pass

if __name__ == "__main__":
    app.run(debug=True, port=8080)
