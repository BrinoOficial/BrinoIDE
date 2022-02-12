#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO Matar arquivo

"""
Br.ino Qt plataforma contribuida

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


class PlataformaContribuida:
    def __init__(self, data, parent):
        self.nome = data['name']
        self.pacote = parent
        self.arq = data['architecture']
        self.versao = data['version']
        self.categoria = data['category']
        self.placas = data['boards']
        self.ferramentas = data['toolsDependencies']
        self.ferramentas_resolvidas = dict()
        self.pasta_instalada = ""

    def get_ferramentas_resolvidas(self):
        return self.ferramentas_resolvidas.values()

    def resolver_dependencias_ferramentas(self):
        for tool in self.ferramentas:
            self.ferramentas_resolvidas[tool['name']] = self.pacote.get_ferramenta_por_nome(tool['name'])

    def get_pasta_instalada(self):
        return self.pasta_instalada

    def get_arquitetura(self):
        return self.arq

    def get_versao(self):
        return self.versao

    def set_pasta_instalada(self, pasta):
        self.pasta_instalada = pasta

    def get_nome(self):
        return self.nome
