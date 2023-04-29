"""
    AD - Trabalho 03 - client.py
    Manuel Barral 56943, Lilia Colisnyc xxxxx

"""
import requests
import json
import sys

def avalcmnd (cmnd):
    return True

while True:
    cmnd = input("Input comand here ...> ")
    operation = cmnd.split()[0]
    
    if cmnd == "EXIT":
        break 
    elif avalcmnd(cmnd) == True:
        if operation == "SEARCH":
        # Param: <location> <cost> 
        # Given a <cost> and <location>, returns all trips until said <cost> based on the <location>
            r = requests.get('http://127.0.0.1:8082/search/' + cmnd.split()[1]+ "/"+ cmnd.split()[2])
            print(r.status_code)
            print(r.content.decode())

        elif operation == "FILTER":
            
            if cmnd.split()[1] == "DIVERSIFY":
                pass
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
            pass
    else:
        print("Unknown Command")

print('Programa Encerrado')