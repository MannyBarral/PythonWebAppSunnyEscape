"""
    AD - Trabalho 03 - client.py
    Manuel Barral 56943, Lilia Colisnyc xxxxx

"""
import requests
import json
import sys


while True:
    cmnd = input("Input comand here ...> ")
    operation = cmnd.split()[0]
    
    if cmnd == "EXIT":
        break 

    if operation == "SEARCH":
    # Param: <location> <cost> 
    # Given a <cost> and <location>, returns all trips until said <cost> based on the <location>
        if len(cmnd.split()) == 3:
            if type(cmnd.split()[1]) == str:
                if int(cmnd.split()[2]) != None:
                    r = requests.get('http://127.0.0.1:8082/search/' + cmnd.split()[1]+ "/"+ cmnd.split()[2])
                    print(r.status_code)
                    print(r.content.decode())
                elif type(cmnd.split()[2]) !=  int:
                    print("COST PARAMETER MUST BE A VARIABLE TYPE INTEGER")
            elif type(cmnd.split()[1]) != str:
                print("LOCATION PARAMETER MUST BE A VARIABLE TYPE STRING")
        elif len(cmnd.split()) < 3:
            print('MISSING ARGUMENTS')
        elif len(cmnd.split()) > 3:
            print('TOO MANY ARGUMENTS')

    elif operation == "FILTER":
        
        if cmnd.split()[1] == "DIVERSIFY":
            r = requests.get('http://127.0.0.1:8082/filter/diversify')
            print(r.status_code)
            print(r.content.decode())
        else:
        # Param: DST <location> AIRLINE <code> SUN <n>, where 2 <= n <=4
        # given a <location> a <code> and <n>, as well as a list of travel IDs the server must filter and
        # return just the trips available to the <location> in company <code> with exactly <n> days of 
        # sunshine
            pass

    elif operation == "DETAILS":
    # Param: <viagem_ID>
    # Given a <viagem_ID> the server will return a detailed preview of the trip:
    # 4 days of travel + costs + all the data of the two flights (dates, origin and destination, IATAs, etc...)
        if len(cmnd.split()) == 2:
                r = requests.get('http://127.0.0.1:8082/details/' + cmnd.split()[1])
                print(r.status_code)

                if r.content.decode() == "FlightNotFound":
                    print('NO FLIGHT INFORMATION AVAILABLE OR FLIGHT DOSEN´T EXIST')
                else:
                    print(r.content.decode())
        elif len(cmnd.split()) < 2:
            print('MISSING ARGUMENTS')
        elif len(cmnd.split()) > 2:
            print('TOO MANY ARGUMENTS')
    else:
        print("Unknown Command")

print('Programa Encerrado')