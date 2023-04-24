"""
    AD - Trabalho 03 - client.py
    Manuel Barral 56943, Lilia Colisnyc xxxxx

"""
import requests
import json
import sys

def avalcmnd (cmnd):
    pass

while True:
    cmnd = input()
    operation = input.split()[0]
    if cmnd == "EXIT":
        break 
    if avalcmnd(cmnd) == True:
        if operation == "SEARCH":
            pass 
        if operation == "FILTER":
            pass
        if operation == "DETAILS":
            pass
    else:
        "Unknown Command"

print('Programa Encerrado')