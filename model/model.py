import copy

import networkx as nx
from database.dao import DAO
from operator import itemgetter
class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._artists = None

        self.sol_ottimale = []
        self.peso_max = 0



    def load_all_artists(self,n_alb):
        self._artists = DAO.get_all_artists(n_alb)
        print(f"Artisti: {self._artists}")

    def build_graph(self):
        self._graph.clear()

        self._graph.add_nodes_from(self._artists.values())

        self._edges = DAO.get_conessioni(self._artists)

        for edge in self._edges:
            artista1 = self._artists[edge[0]]
            artista2 = self._artists[edge[1]]

            self._graph.add_edge(artista1, artista2, weight=self._edges[edge])
        return len(self._graph.nodes), len(self._graph.edges)

    def artisti_collegati(self,a):
        artista = self._artists[a]
        conessi = list(nx.node_connected_component(self._graph,artista))
        conessi.remove(artista)
        risultato =[]
        for conesso in conessi:
            print(artista)
            print(conesso)
            peso = self._graph[artista][conesso]['weight']
            risultato.append((conesso,peso))
        risultato = sorted(risultato, key=itemgetter(1),reverse=True)
        return risultato

    def ricerca_cammino(self,d,num_art,art):
        parziale = [art]
        peso = 0

        self.ricorsione(parziale,peso,d,num_art)

        return self.sol_ottimale

    def ricorsione(self,parziale,peso,d,num_art):
        ultimo = parziale[-1]
        amissibili = self.get_amissibili(ultimo,parziale,d)


        if len(amissibili)==0:
            if peso > self.peso_max and len(parziale)<num_art:
                self.sol_ottimale = copy.deepcopy(parziale)
                peso = copy.deepcopy(peso)

        for n in amissibili:
            parziale.append(n)
            peso += self._graph[ultimo][n]['weight']
            self.ricorsione(parziale,peso,d,num_art)
            parziale.pop()
            peso -= self._graph[ultimo][n]['weight']


    def get_amissibili(self,ultimo,parziale,d):
        art_d_min = DAO.get_d_min(d)
        amissibili = []
        vicini = self._graph.neighbors(ultimo)
        for vicino in vicini:
            if vicino not in parziale and vicino.id in art_d_min:
                amissibili.append(vicino)
        return amissibili