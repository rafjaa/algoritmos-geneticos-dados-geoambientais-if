# coding: utf-8

import json
import time
from flask import Flask
from flask import jsonify, request, render_template
from modulos import geneticista, graficos

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/genesis', methods=['GET'])
def genesis():
    '''
        Recebe os parâmetros da interface web e executa o algoritmo genético.
        Persiste o estado da última execução e retorna um JSON com o resultado.
    '''

    if request.method == 'GET':
        tamanho_populacao = int(request.args.post('tamanho_populacao'))
        quantidade_melhores = int(request.args.post('quantidade_melhores'))
        numero_geracoes = int(request.args.post('numero_geracoes'))
        percentual_mutacao = int(request.args.post('percentual_populacao')) / 100.
        ponto_inicial = request.args.post('ponto_inicial')

        # Tempo de execução
        tempo_inicial = time.time()

        populacao = geneticista.Populacao(tamanho_populacao, quantidade_melhores, numero_geracoes, percentual_mutacao, ponto_inicial)
       
        tempo_execucao = time.time() - tempo_inicial

        evolucao = []
        

        while True:
            geracao = populacao.proxima_geracao()

            if not geracao:
                break
           
            geracao.reverse()
            evolucao.append(geracao)

        json.dump(evolucao, open('temp/geracoes.json', 'w'))
        melhor_individuo = populacao.melhor_da_geracao()

        return jsonify(rota=melhor_individuo.copia_rota(), peso=melhor_individuo.peso(), tempo_execucao=tempo_execucao)


@app.route('/grafico/geracoes')
def grafico_geracoes():
    AMOSTRAGEM = 20 # Porcentagem

    geracoes = json.load(open('dados/geracoes.json'))
    marcador = len(geracoes) / AMOSTRAGEM

    amostra = []

    for i, j in enumerate(geracoes):
         if not i % marcador:
            amostra.append(j)

    graficos.grafico_geracoes(amostra)

    return ''


@app.route('/grafico/convergencia')
def grafico_convergencia():
    geracoes = json.load(open('dados/geracoes.json'))
    evolucao = [g[-1] for g in geracoes]
    graficos.grafico_convergencia(evolucao)
    return ''


if __name__ == '__main__':
    app.run(port=8000)