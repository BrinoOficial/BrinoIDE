"""
Br.ino Qt Pacote Alvo

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


class PacoteAlvo:

    def __init__(self, id_):
        self.id_ = id_
        self.plataformas = dict()

    def get_plataformas(self):
        """

        :return:
            None
        """
        return self.plataformas

    def get_lista_plataformas(self):
        """

        :return:
            None
        """
        return self.plataformas.values()

    def get(self, plataforma):
        """

        :param plataforma:
        :return:
            None
        """
        return self.plataformas.get(plataforma)

    def tem_plataforma(self, plataforma):
        """

        :param plataforma:
        :return:
            None
        """
        return plataforma.get_id() in self.plataformas

    def get_id(self):
        """

        :return:
            None
        """
        return self.id_

    def adicionar_plataforma(self, plataforma):
        """

        :param plataforma:
        :return:
            None
        """
        self.plataformas[plataforma.get_id()] = plataforma
