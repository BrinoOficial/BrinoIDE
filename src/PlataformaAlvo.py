#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Br.ino Qt plataforma alvo

Interface base da IDE Br.ino
em PyQt5 (python 3.6)

    IDE do Br.ino  Copyright (C) 2018  Br.ino

    Este arquivo e parte da IDE do Br.ino.

    A IDE do Br.ino e um software livre: voce pode redistribui-lo
    e / ou modifica-lo de acordo com os termos da Licenca Publica
    Geral GNU, conforme publicado pela Free Software Foundation,
    seja a versao 3 da Licenca , ou (na sua opcao) qualquer
    versao posterior.

    A IDE do Br.ino e distribuida na esperanca de que seja util,
    mas SEM QUALQUER GARANTIA sem a garantia implicita de
    COMERCIALIZACAO ou ADEQUACAO A UM DETERMINADO PROPOSITO.
    Consulte a Licenca Publica Geral GNU para obter mais detalhes.

    Voce deveria ter recebido uma copia da Licenca Publica Geral
    GNU junto com este programa. Caso contrario, veja
    <https://www.gnu.org/licenses/>

    Codigo fonte baseado no codigo do arduino

website: brino.cc
modificado por: Mateus Berardo
email: mateus.berardo@brino.cc
modificado por: Victor Rodrigues Pacheco
email: victor.pacheco@brino.cc
"""

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
            print("no boards.txt")
        pref_placas = MapaUtils.carregar(arquivo_placas)
        preferencias_placas = MapaUtils.primeiro_nivel(pref_placas)
        menu = preferencias_placas['menu']
        if len(menu) > 0:
            self.menus = MapaUtils.dicionario_superior(menu)
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

    def get_ferramenta(self, tool):
        return MapaUtils.sub_tree(MapaUtils.sub_tree(self.get_preferencias(), "tools"), tool)

    def get_menus(self):
        return self.menus;
