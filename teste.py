from flask import Flask, jsonify, json, abort, request
import urllib.request

app = Flask(__name__)

print("Carregando dados do json em memoria")
json_de_imoveis = urllib.request.urlopen(
    "https://raw.githubusercontent.com/VivaReal/code-challenge/master/properties.json").read().decode('utf-8')
json_de_imoveis = json.JSONDecoder().decode(json_de_imoveis)  

json_de_bairros = urllib.request.urlopen(
    "https://raw.githubusercontent.com/VivaReal/code-challenge/master/provinces.json").read().decode('utf-8')
json_de_bairros = json.JSONDecoder().decode(json_de_bairros)

@app.route('/properties/', methods=['POST'])
def properties_create():
    json_de_dados = request.json

    if not all(
        keys in json_de_dados for keys in (
            'beds',
            'baths',
            'x',
            'y',
            'title',
            'price',
            'description',
            'squareMeters')):
        abort(400)

    if json_de_dados['baths'] < 1 or json_de_dados['baths'] > 4:
        abort(400)

    if json_de_dados['beds'] < 1 or json_de_dados['beds'] > 5:
        abort(400)

    if json_de_dados['squareMeters'] < 20 or json_de_dados['baths'] > 240:
        abort(400)

    if json_de_dados['x'] < 0 or json_de_dados['x'] > 1400:
        abort(400)

    if json_de_dados['y'] < 0 or json_de_dados['y'] > 1000:
        abort(400)

    ultimo_id = json_de_imoveis['properties'][-1]['id']

    json_de_dados['id'] = ultimo_id + 1
    json_de_dados['lat'] = json_de_dados['x']
    json_de_dados['long'] = json_de_dados['y']

    json_de_dados.pop('x')
    json_de_dados.pop('y')

    json_de_imoveis['properties'].append(json_de_dados)

    return "Created", 201


@app.route('/properties/<int:id>')
def properties_show(id):
    imovel = [el for el in json_de_imoveis['properties'] if el['id'] == id]
    if len(imovel) == 0:
        abort(404)

    if len(imovel) > 1:
        abort(500)

    imovel = imovel[0]
    imovel['provinces'] = buscaBairro(imovel['lat'], imovel['long'])

    return jsonify(imovel)


@app.route('/properties/', methods=['GET'])
def properties_index():
    x1 = int(request.args.get('ax'))
    x2 = int(request.args.get('bx'))
    y1 = int(request.args.get('ay'))
    y2 = int(request.args.get('by'))

    imoveis = [el for el in json_de_imoveis['properties'] if el['lat'] >=
               x1 and el['lat'] <= x2 and el['long'] >= y1 and el['long'] <= y2]
    for imovel in imoveis:
        imovel['provinces'] = buscaBairro(imovel['lat'], imovel['long'])

    result = {
        'foundProperties': len(imoveis),
        'properties': imoveis
    }

    return jsonify(result)


def buscaBairro(x, y):
    bairros = []
    for bairro in json_de_bairros:
        x1 = json_de_bairros[bairro]['boundaries']['upperLeft']['x']
        x2 = json_de_bairros[bairro]['boundaries']['bottomRight']['x']
        y1 = json_de_bairros[bairro]['boundaries']['upperLeft']['y']
        y2 = json_de_bairros[bairro]['boundaries']['bottomRight']['y']
        if x >= x1 and x <= x2 and y <= y1 and y >= y2:
            bairros.append(bairro)

    return bairros
