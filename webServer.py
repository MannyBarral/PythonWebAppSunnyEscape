"""
    AD - Trabalho 03 - webServer.py
    Manuel Barral 56943, Lilia Colisnyc xxxxx

"""
from flask import Flask, request, make_response, jsonify
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
        cursor.execute("CREATE TABLE airlines (code TEXT, name TEXT)") # Criação da tabela airlines
        # Inicializar a tabela locations com 10 registos:
        registos = [(0,'Lisboa','LIS','Lisbon'),
            (1,'Madrid','MAD','Madird'),
            (2,'Paris','CDG','Paris'),
            (3,'Dublin','DUB','Dublin'),
            (4,'Brussels','BRU','Brussels'),
            (5,'Liubliana','LJU','Ljubljana'),
            (6,'Amsterdam','AMS','Amsterdam'),
            (7,'Berlin','TXL','Berlin'),
            (8,'Roma','FCO','Roma'),
            (9,'Vienna','VIE','Vienna')]
        # cursor.execute("INSERT INTO locations VALUES (?,?,?,?)", registos)
        for i in registos:
            cursor.execute("INSERT INTO locations VALUES (?,?,?,?)", i)
        connection.commit()
    return connection, cursor
        
connectDB("flightsDB.db")

@app.route('/search')
@app.route('/search/<location>/<int:cost>')
def search(location=None, cost=None):
    if request.method == 'GET':    
        conn, cursor = connectDB("flightsDB.db")
        conn.commit()
        conn.close()
        r = make_response(jsonify("Placeholder for response to search: viagens (roundtrips) from location to another under price stipulated"))
        r.status_code = 200
        return r

@app.route('/filter', methods= ['GET'])
def filter ():
    pass

@app.route('/details', methods=['GET'])
def details ():
    pass

if __name__ == "__main__":
    app.run(debug=True, port=8081)
