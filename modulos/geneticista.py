# -*- coding: utf-8 -*-

import random
from string import ascii_lowercase

class Individuo:
    
    def __init__(self, base=None, origem=None, dna=None):
        self._peso = 0

        # gera o indivíduo com o dna informado
        if dna:
            self._dna = dna
            self._origem = dna[0]
            return

        # gera um indivíduo com um dna aleatório e origem informada, a partir da base informada
        if base and origem:
            self._origem = origem
            self._dna = self._gera_dna(base[:])

    def _gera_dna(self, base):
        base.remove(self._origem)
        random.shuffle(base)
        return list(self._origem) + base

    def __str__(self):
        return ' - '.join(self._dna)

    def __add__(self, parceira):
        # define dois pontos de corte
        i, j = random.randint(1, len(self._dna) - 1), random.randint(1, len(self._dna) - 1)

        # garante pontos de corte distintos
        while i == j:
            j = random.randint(1, len(self._dna) - 1)

        # garante que i seja o menor entre i e j
        if i > j:
            i, j = j, i

        # obtém cópias dos dnas dos indivíduos do cruzamento
        dna_parceira = parceira.copia_dna()
        dna_individuo = self.copia_dna()
        corte_dna_parceira =  dna_parceira[i:j]
        corte_dna_individuo = dna_individuo[i:j]

        extremidade = len(dna_parceira) - j

        # gera o primeiro filho
        # genes da parceira que não estão no bloco de corte do indivíduo
        auxiliar_genetico = [d for d in dna_parceira[j:] + dna_parceira[:j] if d not in corte_dna_individuo]
        
        dna_filho = auxiliar_genetico[extremidade:] + corte_dna_individuo + auxiliar_genetico[:extremidade]

        # gera o segundo filho
        # genes do indivíduo que não estão no bloco de corte da parceira
        auxiliar_genetico = [d for d in dna_individuo[j:] + dna_individuo[:j] if d not in corte_dna_parceira]
        dna_filha = auxiliar_genetico[extremidade:] + corte_dna_parceira + auxiliar_genetico[:extremidade]

        # rotaciona o dna dos filhos, garantindo que tenham o mesmo ponto inicial e preservem os trechos dos cortes recebidos
        dna_filho = dna_filho[dna_filho.index(self._origem):] + dna_filho[:dna_filho.index(self._origem)]
        dna_filha = dna_filha[dna_filha.index(self._origem):] + dna_filha[:dna_filha.index(self._origem)]

        # retorna a tupla com os dnas dos dois filhos gerados
        return (Individuo(dna=dna_filho), Individuo(dna=dna_filha))

    def copia_dna(self):
        return self._dna[:]
        

if __name__ == '__main__':
    base = list(ascii_lowercase)

    adao = Individuo(base, 'a')
    eva = Individuo(base, 'a')    

    print "Adão"
    print adao
    print "Eva"
    print eva
    filhos = eva + adao
    print "Abel"
    print filhos[0]
    print "Caim"
    print filhos[1]
