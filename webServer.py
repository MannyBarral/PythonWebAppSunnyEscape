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
        cursor.execute("CREATE TABLE weather (date INTEGER, location TEXT, condition TEXT, mintemp_c INTEGER, maxtemp_c INTEGER, \
                    PRIMARY KEY(date, location));") # Create table weather with key - (date,location)
        cursor.execute("CREATE TABLE locations (id INTEGER, name TEXT, IATA TEXT, wea_name TEXT);") # Criação da tabela locations 
        cursor.execute("CREATE TABLE legs (id TEXT, dep_IATA TEXT, arr_IATA TEXT, dep_datetime INTEGER, arr_datetime INTEGER,\
                        duration_min INTEGER, arlineCodes TEXT);") # Criação da tabela legs (voos)
        cursor.execute("CREATE TABLE roundtrips (id INTEGER, cost INTEGER, id_leg0 TEXT, id_leg1 TEXT);") # Criação da tabela 
        cursor.execute("CREATE TABLE airlines (code TEXT, name TEXT);") # Criação da tabela airlines
        # Inicializar a tabela locations com 10 registos:
        registos = [(0,'Lisboa','LIS','lisbon'),
            (1,'Paris','CDG','Paris'),
            (2,'Dublin','DUB','Dublin'),
            (3,'Bruxelas','BRU','Brussels'),
            (4,'Atenas','ATH','Athens'),
            (5,'Amsterdão','AMS','Amsterdam'),
            (6,'Berlim','TXL','Berlin'),
            (7,'Roma','FCO','Rome'),
            (8,'Vienna','VIE','Vienna')]
        # cursor.execute("INSERT INTO locations VALUES (?,?,?,?)", registos)
        for i in registos:
            cursor.execute("INSERT INTO locations VALUES (?,?,?,?)", i)
        connection.commit()
    return connection, cursor
        
connectDB("flightsDB.db")

def sunnyPlaner(city):
    """Searches the weather database for possible 4 day trips where there is at least 2 sunny/clear days

    Args:
        city (string): city on which we search for sunny days 

    Returns:
        String: A list of sunny days,(For Now) !!!!!!!!!!
    """     
    conn, cursor = connectDB('flightsDB.db')

    accceptable_days = []
    cursor.execute('SELECT date FROM weather WHERE location = ? AND condition = "Sunny" \
                   OR condition = "Clear"', (city,))
    sunny_clear_days = cursor.fetchall()
    conn.commit()
    for i in sunny_clear_days:
        accceptable_days.append(i)
    if len(accceptable_days) >= 2:
        return accceptable_days
    


@app.route('/search')
@app.route('/search/<location>/<int:cost>')
def search(location=None, cost=None):
    if request.method == 'GET':    
        # Get from WeatherAPI the conditions of the other 9 possible destinations for the next 14 days:
        conn, cursor = connectDB('flightsDB.db')
        cursor.execute("SELECT wea_name FROM locations WHERE name != ?", (location,))
        names = cursor.fetchall()
        conn.commit()
        cities_wea_names = []
        for i in names:
            for x in i:
                cities_wea_names.append(x)
        # For each city search for the weather for the next 14 days        
        for city in cities_wea_names:
            # Per Possible City

            urlWeatherAPI = f'http://lmpinto.eu.pythonanywhere.com/v1/forecast.json?key={api_key}&q={city}&days=14&aqi=no&alerts=no' # URL do Professor
            #urlWeatherAPI = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city}&days=14&aqi=no&alerts=no' #Weather API URL
            req= requests.get(urlWeatherAPI)
            if req.content != b'Cidade nao encontrada':
                # If the city exists (in professor´s API)

                print(json.loads(req.content)['location']['name'], ': ') # Prints name of Capital
                forecast_days = json.loads(req.content)['forecast']['forecastday']
                for i in forecast_days:
                    print(i['date'], ": ", i['day']['condition']['text']) # Prints dates and Weather conditions on those days. 
                # Populate the table weather, location == city
                    date = i["date"]
                    condition = i['day']['condition']['text']
                    min_temp = i['day']['mintemp_c']
                    max_temp = i['day']['maxtemp_c']
                    cursor.execute("INSERT into WEATHER (date, location, condition, mintemp_c, maxtemp_c) VALUES (?,?,?,?,?);",\
                                   (date, city, condition, min_temp, max_temp))
                    conn.commit()
                # Define possible destinations in which there is ,at least, 2 sunny/clear days out of 4:
                print(sunnyPlaner(city))
                # Populate the table airlines:
                dep_date = None
                arr_date = None
                cabin_class = 'Economy'
                currency = 'EUR'
                urlFlightRoundtrip = f'http://lmpinto.eu.pythonanywhere.com/roundtrip/{api_key}/{location}/{city}/{dep_date}/{arr_date}/1/0/0/{cabin_class}/{currency}' #URL Professor

            else:
                print(city, ": Não foi Encontrada")
        r = make_response(jsonify("Placeholder for response to search: viagens (roundtrips) from location to another under price stipulated"))
        r.status_code = 200
        conn.close() # Closes connection to flightsDB
        return r

@app.route('/filter', methods= ['GET'])
def filter ():
    pass

@app.route('/details', methods=['GET'])
def details ():
    pass

if __name__ == "__main__":
    app.run(debug=True, port=8081)
