# -*- coding: utf-8 -*-
import dijkstra
import random

class Conexoes:
	'''
		Possui as distâncias das conexões diretas e as conexões indiretas possíveis entre todos os pontos
		informados no arquivo "nome_arquivo" informado no construtor.
	'''

	def __init__(self,nome_arquivo):
		'''
			Inicializa o objeto com as conexões diretas existentes no arquivo "nome_arquivo".
			Cria as conexões indiretas possíveis a partir das conexões diretas.
		'''
		self._diretas = self._do_arquivo(nome_arquivo)
		self._indiretas = self._gerar_indiretas()

	def distancia(self, i, j):
		'''
			Retorna a distância entre dois pontos i e j, se estes possuírem conexão direta. Caso contrário, retorna None.
		'''
		return None if i == j or i not in self._diretas or j not in self._diretas[i] else self._diretas[i][j]

	def pontos(self):
		'''
			Retorna uma lista com todos os pontos que são chaves no dicionário de conexões diretas
		'''
		return sorted(self._diretas.keys())

	def sub_rota(self,i,j):
		'''
			Retorna uma rota para a conexão entre dois pontos i e j que não possuam conexão direta entre si.
			Se os pontos informados possuirem conexão direta ou forem iguais, retorna None.
		'''
		from random import randint

		if i == j or i in self._diretas and j in self._diretas[i]:
			return None
		else:
			return self._indiretas[(i,j)]

	def _do_arquivo(self,nome_arquivo):
		'''
			Lê o conteúdo do arquivo "nome_arquivo" e retorna um dicionário de conexões diretas.
		'''
		# Lê o conteúdo do arquivo, separando as linhas.
		arquivo = open(nome_arquivo,'r')
		linhas = arquivo.read().split('\n')
		arquivo.close()

		# Expressão regular para validação do formato de texto das linhas.
		import re
		validar = re.compile(r'([a-zA-Z]+[0-9]*;){2}[0-9]+(\.[0-9]+)?;?')
		
		distancias = {}
		for l in linhas:
			if validar.match(l):
				# Separa os dados da linha.
				partes = l.split(';')
				i, j, distancia = partes[0], partes[1], float(partes[2])

				# Se os dados forem válidos, prossegue com a adição.
				if i != j and distancia > 0:
					# Adiciona a distancia no sentido convencional.
					if not i in distancias:
						distancias[i] = {}					
					distancias[i][j] = distancia

					# Se a linha foi quebrada em apenas três partes, significa que a rota é de duplo sentido.
					if len(partes)==3:
						# Adiciona a distância no sentido inverso.
						if not j in distancias:
							distancias[j] = {}
						distancias[j][i] = distancia

		# Retorna o dicionário com as distâncias encontradas
		return distancias

	def _gerar_indiretas(self):
		'''
			Cria e retorna um dicionário de conexões indiretas entre todos os pontos.
			Preserva toda a variedade de rotas para um mesmo para de pontos.
		'''
		indiretas = {}
		
		# Gera as conexões (rotas) indiretas para cada ponto existente em self._diretas
		for i in self._diretas.keys():
			for j in self._diretas.keys():
				if i != j and j not in self._diretas[i]:
					indiretas[(i,j)] = dijkstra.shortestPath(self._diretas, i, j)

		# retorna o dicionário criado
		return indiretas

class Individuo:
    '''
        Contém todos os dados e ações referentes a um indivíduo: rota, peso, cruzamento, etc.
    '''
    # Define para a classe um objeto de conexões, permitindo definir o peso do indivíduo e
    # obter conexões indiretas para o indivíduo, se necessário.
    _conexoes = Conexoes('distancias.dat')
    # Define para a classe ausência de mutação. Poderá ser moficado externamente.
    taxa_mutacao = 0
    # Mantém na classe um dicionário com os pesos das conexões indiretas já avaliadas, evitando repetição de cálculos
    _avaliadas = {}


    def __init__(self, origem=None, especifico=None):
        '''
            O construtor permite gerar um indíviduo com rota aleatória partindo de um ponto específico
            ou criar um indivíduo com uma rota pré-determinada.
            Ao informar uma rota, é permitido informar todas ou algumas sub-rotas a serem utilizadas.
            Se necessário adiciona sub-rotas aleatoriamente à rota de um indivíduo, seja ela gerada
            aleatoriamente ou pré-determinada.

            Para definir qual método será adotado, basta definir SOMENTE UM dos parâmetros do construtor:

                origem (str)-> define a criação de um indovíduo com rota aleatória iniciada no ponto "origem" 
                
                especifico (list) -> define a criação de um indivíduo com rota e sub-rotas especificas.
                    especifico[0] -> rota a ser utilizada
                    especifico[1] -> lista de sub-rotas a serem utilizadas
        '''

        # gera um indivíduo com uma rota aleatória iniciada na origem informada
        if origem and origem in self._conexoes.pontos():
            self._origem = origem
            self._rota = self._gera_rota()
            self._sub_rotas = {}
            self._peso = self._avaliar_peso()
        # gera o indivíduo com a rota informada, se os dados forem válidos
        elif especifico and sorted(especifico) == sorted(self._conexoes.pontos()):
            self._origem = especifico[0]
            self._rota = especifico
            self._peso = self._avaliar_peso()

    def __str__(self):
        '''
            APAGAR ESSA FUNCAO ????????????????????????????????????????????????????????????????????
        '''
        retorno = ' - '.join(self._rota)
        retorno += '\n Peso: ' + str(self._peso)
        return retorno

    def __add__(self, parceira):
        '''
            Realiza o cruzamento entre o indivíduo e a parceira informada, gerando dois filhos.
        '''
        # define dois pontos de corte
        i, j = random.randint(1, len(self._rota) - 1), random.randint(1, len(self._rota) - 1)

        # garante que os pontos de corte sejam distintos
        while i == j:
            j = random.randint(1, len(self._rota) - 1)

        # garante que i seja o menor entre i e j
        if i > j:
            i, j = j, i

        # obtém cópias das rotas dos indivíduos do cruzamento
        rota_parceira = parceira.copia_rota()
        rota_individuo = self.copia_rota()
        corte_rota_parceira =  rota_parceira[i:j]
        corte_rota_individuo = rota_individuo[i:j]

        limite = len(rota_parceira) - j

        # gera o filho
        # genes da parceira que não estão no bloco de corte do indivíduo
        auxiliar_genetico = [d for d in rota_parceira[j:] + rota_parceira[:j] if d not in corte_rota_individuo]
        rota_filho = auxiliar_genetico[limite:] + corte_rota_individuo + auxiliar_genetico[:limite]

        # gera a filha
        # genes do indivíduo que não estão no bloco de corte da parceira
        auxiliar_genetico = [d for d in rota_individuo[j:] + rota_individuo[:j] if d not in corte_rota_parceira]
        rota_filha = auxiliar_genetico[limite:] + corte_rota_parceira + auxiliar_genetico[:limite]

        # gira a rota dos filhos, de modo que tenham o mesmo ponto inicial e preservem os trechos dos cortes herdados
        rota_filho = rota_filho[rota_filho.index(self._origem):] + rota_filho[:rota_filho.index(self._origem)]
        rota_filha = rota_filha[rota_filha.index(self._origem):] + rota_filha[:rota_filha.index(self._origem)]

        # executa a função de mutação (poderá mutar ou não, aleatoriamente) sobre os filhos
        self._mutar(rota_filho)
        self._mutar(rota_filha)

        # cria os filhos com suas respectivas rotas e sub-rotas herdadas
        filho = Individuo(especifico=rota_filho)
        filha = Individuo(especifico=rota_filha)

        # retorna a tupla com os dois filhos gerados
        return (filho,filha)

    def _gera_rota(self):
        '''
            Gera uma rota aleatória iniciada no ponto self._origem, seguindo todos os pontos de self._conexao.
        '''
        base = self._conexoes.pontos()
        base.remove(self._origem)
        random.shuffle(base)
        return [self._origem] + base

    def _avaliar_peso(self, sub_rota=None):
        '''
            Avalia o peso(soma das distâncias da rota e das sub-rotas) de um indivíduo.
            Como o indíviduo pode ter herdado sub-rotas, se for gerador por cruzamento,
            antes de atribuir uma sub-rota aleatória para um par de pontos sem conexão direta
            verifica se o mesmo já possui alguma para uso.

            A função é utiliza para calcular também o peso de uma sub-rota. Nesse caso, basta especificar
            o parâmetro sub_rota como uma lista/tupla de três elementos: inicial, final e índice.
        '''
        peso = 0

        # se sub_rota for None, avalia o dna do próprio objeto
        if not sub_rota:
            # acumula o peso de cada par de índices (incluindo o retorno)
            tamanho = len(self._rota)
            for i in xrange(tamanho):
                # define os índices atuais
                a = self._rota[i]
                b = self._rota[(i+1)%tamanho]

                # calcula o peso da ligação
                aux_peso = self._conexoes.distancia(a, b)
                # se não houve peso (conexão direta), calcula o peso da subrota
                if not aux_peso:
                    # verifica se o indivíduo já possui uma sub-rota para o par de índices, se não tiver, solicita uma.
                    aux_peso = self._avaliar_peso(self._conexoes.sub_rota(a,b))

                peso += aux_peso

        # calcula e retorna o peso de uma sub-rota informada
        else:
            # separa o parâmetro
            i = sub_rota[0]
            f = sub_rota[-1]
            # aproveita o cálculo já efetuado, se existir
            if i in self._avaliadas and f in self._avaliadas[i]:
                peso = self._avaliadas[i][f]
            else:
                # calcula o peso da sub-rota
                for x in xrange(len(sub_rota)-1):
                    peso += self._conexoes.distancia(sub_rota[x], sub_rota[x+1])
                # memoriza o peso calculado
                if i not in self._avaliadas:
                    self._avaliadas[i] = {}
                if f not in self._avaliadas[i]:
                    self._avaliadas[i][f] = peso

        # retorna o peso acumulado
        return peso

    def peso(self):
        '''
            Retorna o peso do indivíduo.
        '''
        return self._peso

    def _mutar(self, rota):
        '''
            Executa uma mutação sobre uma rota, trocando dois de seus pontos aleatórios de lugar.
        '''
        # define (aleatoriamente) se deve ou não mutar
        if self.taxa_mutacao == 0 or self.taxa_mutacao < random.random():
            return False

        # sorteia dois pontos de troca distintos
        ponto1 = random.randint(1,len(rota)-1)
        ponto2 = random.randint(1,len(rota)-1)
        while ponto1 == ponto2:
            ponto2 = random.randint(0,len(rota)-1)

        # efetua a troca
        rota[ponto1], rota[ponto2] =rota[ponto2], rota[ponto1]

        return True
    
    def copia_rota(self):
        '''
            Retorna uma cópia da rota do indivíduo.
        '''
        return self._rota[:]

    def copia_sub_rota(self,i,j):
        '''
            Retorna uma cópia de uma sub-rota i,j do invíduo ou None, se ele não possuí-la.
        '''
        return self._sub_rotas.get((i,j))

class Populacao:

	def __init__(self, tamanho_populacao, quantidade_melhores, total_geracoes, taxa_mutacao, ponto_inicial):
		'''
			Inicializa a população com os parâmetros informados. Se algum parâmetro for inválido, retorna None.
		'''
		
		if tamanho_populacao <= 0 or quantidade_melhores <= 0 or quantidade_melhores > tamanho_populacao or total_geracoes <= 0 or taxa_mutacao<0 or taxa_mutacao>1:
			return None 

		self._tamanho_populacao = tamanho_populacao
		self._quantidade_melhores = quantidade_melhores
		self._total_geracoes = total_geracoes
		Individuo.taxa_mutacao = taxa_mutacao
		self._ponto_inicial = ponto_inicial
		self._populacao = []

		# inicializa o contador de gerações
		self._geracao_atual = 0

	def _ordenar_populacao(self):
		'''	
			Ordena a população, por ordem crescente do peso dos indivíduos.
		'''
		self._populacao.sort(key = lambda i:i.peso())

	def proxima_geracao(self):
		'''
			Gera a próxima geração, preservando os n melhores indivíduos e colocando os filhos
			no lugar dos indivíduos cruzados.
			Retorna uma lista com o peso dos indivíduos da geração atual, em ordem crescente.
		'''

		# se for a primeira geração, apenas preenche a população com indivíduos aleatórios
		if self._geracao_atual == 0:
			# preenche a população
			for i in xrange(self._tamanho_populacao):
				self._populacao.append(Individuo(self._ponto_inicial))
			self._geracao_atual = 1

			# mantém a primeira geração ordenada
			self._ordenar_populacao()
		
		# se ainda possuir gerações possíveis, gera a próxima
		elif self._geracao_atual < self._total_geracoes:
		
			# preserva os 10 melhores
			preservados = []
			for x in xrange(self._quantidade_melhores):
				preservados.append(self._populacao.pop(0))

			# cruza os indivíduos restantes aos pares (aleatórios)
			random.shuffle(self._populacao)
			novos = []
			for x in xrange(len(self._populacao) / 2):
				novos.extend(self._populacao.pop() + self._populacao.pop())

			# atualiza a população da geração atual (10 melhores, filhos gerados e talvez 1 indivíduo não cruzado)
			self._populacao += preservados
			self._populacao += novos
			self._ordenar_populacao()

			self._geracao_atual += 1

		# não há mais gerações a criar
		else:
			return None

		# retorna uma lista com o peso dos indivíduos da geração atual, em ordem crescente.
		return [individuo.peso() for individuo in self._populacao]


if __name__=='__main__':
	popu = Populacao(4,1,1000,0.042,'ni')

	while 1:
		p = popu.proxima_geracao()
		if not p:
			break
		print p
