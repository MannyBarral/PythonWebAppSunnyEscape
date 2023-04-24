## WEATHER API FREE - LPINTO
## Emula a weatherapi.com
# para usar fazer o usual: request.get("localhost:9999/v1/forecast.json...")

from flask import Flask, request, make_response
import json


app = Flask(__name__)


# Rota principal
@app.route('/v1/forecast.json', methods=['GET'])
def home():
    print(request)
    q=request.args.get('q')
    print("q:",q)
    
    filename=f'weather_{q}.json'
    print(filename)
    with open(filename, 'r') as f:
        json_content = f.read() # Lê os bytes do arquivo
    # Converte o conteúdo JSON em um objeto Python
    dict = json.loads(json_content)

    
    rsp = make_response(dict)
    rsp.status_code = 200
    return rsp

if __name__ == '__main__':
    app.run(debug=True,port=9999)
