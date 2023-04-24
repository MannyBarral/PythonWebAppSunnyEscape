import json

filename='dados.json'
with open(filename, 'r') as f:
    json_content = f.read() # Lê os bytes do arquivo
# Converte o conteúdo JSON em um objeto Python
dict = json.loads(json_content)

print(dict) # imprimir os dados