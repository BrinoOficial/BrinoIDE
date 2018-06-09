"""
Br.ino Qt indice de contribuicao

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

from PacoteContribuido import PacoteContribuido


class IndiceContribuicao:
    def __init__(self, data=None):
        self.pacotes = dict()
        if data is not None:
            for package in data['packages']:
                pacote = PacoteContribuido(package)
                self.pacotes[pacote.get_id()] = pacote

    def get_plataformas_instaladas(self):
        return self.get_plataformas()

    def get_plataformas(self):
        plataformas = list()
        pacs = self.get_pacotes()
        for pacote in pacs:
            for plataforma in pacote.get_plataformas():
                plataformas.append(plataforma)
        return plataformas

    def get_pacotes(self):
        return self.pacotes.values()

    def adicionar_pacotes(self, dicio):
        self.pacotes.update(dicio)

    def get_pacotes_dicio(self):
        return self.pacotes

    def get_pacote(self, nome):
        return self.get_pacotes_dicio().get(nome)
