## FLIGHT API - FREE - LPINTO
## Emula a flights.io APIcom
# para usar 
# em vez do usual: 
#GET a : https://api.flightapi.io/roundtrip/{apikey}/GRU/JFK/2023-04-04/2023-04-08/1/0/0/Economy/EUR
#fazer:
#GET a : https://localhost:9998/roundtrip/{apikey}/GRU/JFK/2023-04-04/2023-04-08/1/0/0/Economy/EUR

from flask import Flask, request, make_response
import json
from os.path import isfile

app = Flask("Lmpinto Flight API")

# Rota principal
@app.route('/roundtrip/<string:apikey>/<string:src>/<string:dst>/<string:dept>/<string:arri>/1/0/0/Economy/EUR', methods=['GET'])
def home(src,dst,dept,arri,apikey):

    src = src.lower()
    dst = dst.lower()
    arri = arri.replace('-','')
    dept = dept.replace('-','')
    filename=f'voos_{src}_{dst}_{dept}_{arri}.json'
    print(f"Retornando viagens ida-e-volta de {src} para {dst}, nos dias {dept} a {arri}.")
    print(filename)
    if isfile(filename):
        with open(filename, 'r') as f:
            json_content = f.read() # Lê os bytes do arquivo
        # Converte o conteúdo JSON em um objeto Python
        dict = json.loads(json_content)
        rsp = make_response(dict)
        rsp.status_code = 200
    else:
        print(f"file {filename} does not exist")
        rsp = make_response(f"file {filename} does not exist")
        rsp.status_code = 200
    return rsp

if __name__ == '__main__':
    app.run(debug=True,port=9998)
