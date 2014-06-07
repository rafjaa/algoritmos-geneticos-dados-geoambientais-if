#coding: utf-8

from flask import Flask
from flask import jsonify, request
import geneticista
import graficos
import json


app = Flask(__name__)

@app.route('/genesis', methods=['POST'])
def genesis():
    if request.method == 'POST':
        tamanho_populacao = request.args.post('tamanho_populacao')
        numero_geracoes = request.args.post('numero_geracoes')
        percentual_mutacao = request.args.post('percentual_populacao')
        ponto_inicial = request.args.post('ponto_inicial')

        populacao = geneticista.Populacao(tamanho_populacao, numero_geracoes, percentual_mutacao, ponto_inicial)
        return ''

@app.route('/grafico/geracoes')
def grafico_geracoes():
    geracoes = json.load(open('temp/geracoes.json'))
    graficos.grafico_geracoes(geracoes)
    return ''

@app.route('/grafico/convergencia')
def grafico_convergencia():
    geracoes = json.load(open('temp/geracoes.json'))
    evolucao = [g[-1] for g in geracoes]
    graficos.grafico_convergencia(evolucao)
    return ''
            

if __name__ == '__main__':
    app.run()
