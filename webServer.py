"""
    AD - Trabalho 03 - webServer.py
    Manuel Barral 56943, Lilia Colisnyc xxxxx

"""
from flask import Flask, request, make_response, jsonify
import requests
import sqlite3
import json
from os.path import isfile

app = Flask(__name__)

api_key = 'e5b2cb8889174437992143058232404'

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
        registos = [(0,'Lisboa','LIS','lisbon'),
            (1,'Madrid','MAD','madird'),
            (2,'Paris','CDG','paris'),
            (3,'Dublin','DUB','dublin'),
            (4,'Bruxelas','BRU','brussels'),
            (5,'Atenas','LJU','athens'),
            (6,'Amsterdão','AMS','amsterdam'),
            (7,'Berlim','TXL','berlin'),
            (8,'Roma','FCO','rome'),
            (9,'Vienna','VIE','vienna')]
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
        # Get from WeatherAPI the conditions of the other 9 possible destinations for the next 14 days:
        conn, cursor = connectDB('flightsDB.db')
        cursor.execute("SELECT wea_name FROM locations WHERE name != ?", (location,))
        names = cursor.fetchall()
        conn.commit()
        conn.close()
        cities_wea_names = []
        for i in names:
            for x in i:
                cities_wea_names.append(x)
        print(cities_wea_names)
        # For each city search for the weather for the next 14 days        
        for city in cities_wea_names:
            url = f'http://lmpinto.eu.pythonanywhere.com/v1/forecast.json?key={api_key}&q={city}&days=14&aqi=no&alerts=no'
            req= requests.get(url)
            if req.content != b'Cidade nao encontrada':
                print(json.loads(req.content)['location']['name'])
                weathers = []
                for i in 
            else:
                print(city, ": Não foi Encontrada")
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
