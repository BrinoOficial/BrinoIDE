import os

import MapaUtils
from PlacaAlvo import PlacaAlvo


class PlataformaAlvo:

    def __init__(self, arch, pasta, pacote_pai):
        self.id_ = arch
        self.pasta = pasta
        self.pacote_pai = pacote_pai
        self.placas = dict()
        self.placa_padrao = None

        arquivo_placas = os.path.join(pasta, 'boards.txt')
        if not os.path.exists(arquivo_placas):
            print "no boards.txt"
        pref_placas = MapaUtils.carregar(arquivo_placas)
        preferencias_placas = MapaUtils.primeiro_nivel(pref_placas)
        menu = preferencias_placas['menu']
        if len(menu) > 0:
            menus = MapaUtils.dicionario_superior(menu)
        preferencias_placas.pop('menu')
        nome_placas = preferencias_placas.keys()
        for placa in nome_placas:
            preferencias_placa = preferencias_placas[placa]
            self.placas[placa] = PlacaAlvo(placa, preferencias_placa, self)
            if self.placa_padrao is None:
                self.placa_padrao = self.placas[placa]

        self.preferencias = MapaUtils.carregar(os.path.join(pasta, 'platform.txt'))
        self.programador = MapaUtils.primeiro_nivel(MapaUtils.carregar(os.path.join(pasta, 'programmers.txt')))


    def get_preferencias(self):
        return self.preferencias

    def get_id(self):
        return self.id_

    def get_pacote(self):
        return self.pacote_pai

    def get_placas(self):
        return self.placas

    def get_pasta(self):
        return self.pasta

    def get_placa(self, nome):
        if nome in self.placas.keys():
            return self.placas.get(nome)
        return self.placa_padrao
