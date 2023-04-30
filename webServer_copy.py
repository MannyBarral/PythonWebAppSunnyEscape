"""
    AD - Trabalho 03 - webServer.py
    Manuel Barral 56943, Lilia Colisnyc xxxxx

"""
from flask import Flask, request, make_response, jsonify
import requests
import sqlite3
import json
from os.path import isfile
from datetime import datetime, date, timedelta

app = Flask(__name__)

api_key = 'e5b2cb8889174437992143058232404'

today = datetime.combine(date.today(), datetime.min.time())

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
                        duration_min INTEGER, airlineCodes TEXT);") # Criação da tabela legs (voos)
        cursor.execute("CREATE TABLE roundtrips (id TEXT, cost INTEGER, id_leg0 TEXT, id_leg1 TEXT);") # Criação da tabela 
        cursor.execute("CREATE TABLE airlines (code TEXT, name TEXT);") # Criação da tabela airlines
        # Inicializar a tabela locations com 10 registos:
        registos = [(0,'Lisboa','LIS','lisbon'),
            (1,'Paris','ORY','Paris'),
            (2,'Roma','FCO','Rome'),
            (3,'Madird','MAD','Madrid'),
            (4,'Vienna','VIE','Vienna')]
        # cursor.execute("INSERT INTO locations VALUES (?,?,?,?)", registos)
        for i in registos:
            cursor.execute("INSERT INTO locations VALUES (?,?,?,?)", i)
        connection.commit()
    return connection, cursor
        
connectDB("flightsDB2.db")

def sunnyPlaner(city):
    """Searches the weather database for possible 4 day trips where there is at least 2 sunny/clear days

    Args:
        city (string): city on which we search for sunny days 

    Returns:
        List: List of possible 4 day intervals, where there are atleast 2 sunny (first) days
    """     
    conn, cursor = connectDB('flightsDB2.db')
    poss_intervals = []
    accceptable_days = []
    cursor.execute('SELECT date FROM weather WHERE location = ? AND condition = "Sunny" \
                   OR condition = "Clear"', (city,))
    sunny_clear_days = cursor.fetchall()
    conn.commit()
    for i in sunny_clear_days:
        # Puting all sunny/clear dates into acceptable days
        date = datetime.strptime(i[0],'%Y-%m-%d') 
        accceptable_days.append(date)
    
    # Sliding window method for 4 day periods:
    periods = []
    for date in accceptable_days:
        # Makes sure we dont book past day 14 from today´s date
        if date < today + timedelta(days= 10):
            periods.append([date, date + timedelta(days= 1), date + timedelta(days= 2), date + timedelta(days= 3)])
    
    for period in periods:
        counter = 0 
        for day in period:
            if day in accceptable_days:
                counter += 1
        if counter >= 2:
            poss_intervals.append((period[0].date().strftime('%Y-%m-%d'), period[-1].date().strftime('%Y-%m-%d')))
    return poss_intervals


@app.route('/search')
@app.route('/search/<location>/<int:cost>')
def search(location=None, cost=None):
    if request.method == 'GET':    
        # Get from WeatherAPI the conditions of the other 9 possible destinations for the next 14 days:
        conn, cursor = connectDB('flightsDB2.db')
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

                forecast_days = json.loads(req.content)['forecast']['forecastday']
                for i in forecast_days: 
                # Populate the table weather, location == city

                    date = i["date"]
                    condition = i['day']['condition']['text']
                    min_temp = i['day']['mintemp_c']
                    max_temp = i['day']['maxtemp_c']

                    dateCheck = datetime.strptime(date,'%Y-%m-%d') 
                    #if dateCheck >= today:
                    cursor.execute("INSERT into WEATHER (date, location, condition, mintemp_c, maxtemp_c) VALUES (?,?,?,?,?);",\
                                (date, city, condition, min_temp, max_temp))
                    conn.commit()
                # Define possible destinations in which there is ,at least, 2 sunny/clear days out of 4:

                # List with tuples with possible 4 day intervals on witch at least the first two days are sunny 
                poss_intervals = sunnyPlaner(city)

                #Pesquisar na flight API:

                dep_date = "2023-04-26"
                arr_date = "2023-04-29"
                cabin_class = 'Economy'
                currency = 'EUR'
                cursor.execute('SELECT IATA FROM locations WHERE wea_name = ?', (city,))
                capital = cursor.fetchone()[0]
                urlFlightRoundtrip = f'http://lmpinto.eu.pythonanywhere.com/roundtrip/ygyghjgjh/LIS/{capital}/2023-04-26/2023-04-29/1/0/0/Economy/EUR' #URL Professor
                req2 = requests.get(urlFlightRoundtrip)
                legs = json.loads(req2.content)['legs']
                one_way_legs = []
                for leg in legs:
                    if leg['stopoversCount'] == 0:
                        one_way_legs.append(leg)

                # Populate airlines table:
                airlines = json.loads(req2.content)['airlines']
                for airline in airlines:
                    cursor.execute('INSERT into airlines (code, name) VALUES (?,?)', (airline['code'], airline['name']))
                    conn.commit()

                # Populate the legs table
                for owl in one_way_legs:
                    cursor.execute('INSERT into legs (id, dep_IATA, arr_IATA, dep_datetime, arr_datetime, duration_min, airlineCodes)\
                                   VALUES (?,?,?,?,?,?,?)',(owl['id'], owl['departureAirportCode'], owl['arrivalAirportCode'], owl['departureTime'],
                                                           owl['arrivalTime'], owl['duration'], owl['airlineCodes'][0]))
                    conn.commit()
                    
                # Populate table roundtrip
                trips = json.loads(req2.content)['trips']
                fares = json.loads(req2.content)['fares']
                for x in range(len(trips)):
                    cursor.execute('INSERT into roundtrips (id, cost, id_leg0, id_leg1) \
                                   VALUES (?,?,?,?)', (trips[x]['id'] , fares[x]['price']['totalAmount'], trips[x]['legIds'][0], trips[x]['legIds'][1]))
                    conn.commit()

                # Formulate a response with all round trips with cost under the cost stipulated
                response = []
                cursor.execute("SELECT * FROM roundtrips WHERE cost < ?", (cost,))
                trips_under_cost = cursor.fetchall()
                conn.commit()
                for trip in trips_under_cost:
                    response.append(trip)

        r = make_response(jsonify(response))
        r.status_code = 200
        conn.close() # Closes connection to flightsDB
        return r


@app.route('/filter', methods= ['GET'])
@app.route('/filter/diversify', methods= ['GET'])
def filter ():
    if request.method == 'GET':
        
        conn, cursor = connectDB('flightsDB2.db')

        cursor.execute('SELECT * FROM roundtrips;')
        trips = cursor.fetchall()
        
        tripsandcost = {}

        for trip in trips:
            cursor.execute('SELECT arr_IATA FROM legs WHERE id = ?', (trip[2],))
            destinoIATA = cursor.fetchone()

            if destinoIATA != None:
            
                if destinoIATA[0] not in tripsandcost:
                    tripsandcost[destinoIATA[0]] = [[trip[0]], trip[1]]
                else:
                    if trip[1] < tripsandcost[destinoIATA[0]][1]:
                        tripsandcost[destinoIATA[0]] = [[trip[0]], trip[1]]

        response = tripsandcost
        
        r = make_response(jsonify(response))
        r.status_code = 200
        conn.close() # Closes connection to flightsDB
        return r
    
@app.route('/filter/<destination>/<airline>/<int:days>', methods= ['GET'])
def filter2(destination = None, airline = None, days = None):
    pass


@app.route('/details', methods=['GET'])
@app.route('/details/<tripID>', methods= ['GET'])
def details (tripID = None):
    if request.method == 'GET':

        conn, cursor = connectDB("flightsDB2.db")
        response = {}

        cursor.execute('SELECT * FROM roundtrips WHERE id == ?', (tripID,))
        roundTrip = cursor.fetchone()
        
        if roundTrip != None:
            cursor.execute('SELECT * FROM legs WHERE id == ?', (roundTrip[2],))
            firstLegInfo = cursor.fetchone()

            cursor.execute('SELECT * FROM legs WHERE id == ?', (roundTrip[3],))
            secondLegInfo = cursor.fetchone()

            conn.commit() 

            response['tripID'] = tripID
            response['Custo Total'] = roundTrip[1]
            response['First Leg'] = firstLegInfo
            response['second Leg'] = secondLegInfo

        else:
            response = "FlightNotFound"

        r = make_response(jsonify(response))
        r.status_code = 200
        conn.close() # Closes connection to flightsDB
        return r

if __name__ == "__main__":
    app.run(debug=True, port=8082)
