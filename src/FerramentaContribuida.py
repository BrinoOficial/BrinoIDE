"""
Br.ino Qt ferramenta contribuida

Interface base da IDE Br.ino
em PyQt5 (python 2.7)

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

class FerramentaContribuida:
    def __init__(self, data, pacote_pai=None):
        self.pacote = pacote_pai
        self.nome = data['name']
        self.versao = data['version']
        self.sistemas = dict()
        self.pasta_instalada = ""

    def get_nome(self):
        return self.nome

    def get_versao(self):
        return self.versao

    def set_pasta_instalada(self, pasta):
        self.pasta_instalada = pasta

    def get_pasta_instalada(self):
        return self.pasta_instalada
