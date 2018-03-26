"""
Br.ino Qt pacote contribuido

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

from FerramentaContribuida import FerramentaContribuida
from PlataformaContribuida import PlataformaContribuida


class PacoteContribuido:
    def __init__(self, data):
        self.plataformas = dict()
        self.ferramentas = dict()
        self.nome = data['name']
        self.mantenedor = data['maintainer']
        for plat in data['platforms']:
            plataforma = PlataformaContribuida(plat, self)
            self.plataformas[plataforma.get_nome()] = plataforma
        for tool in data['tools']:
            ferramenta = FerramentaContribuida(tool, self)
            self.ferramentas[ferramenta.get_nome()] = ferramenta

    def get_id(self):
        """

        :return:
        """
        return self.nome

    def get_plataformas(self):
        """

        :return:
        """
        return self.plataformas.values()

    def get_ferramentas(self):
        """

        :return:
        """
        return self.ferramentas

    def get_ferramenta_por_nome(self, nome):
        """

        :param nome:
        :return:
        """
        return self.ferramentas[nome]

    def achar_plataforma(self, arquitetura, versao):
        """

        :param arquitetura:
        :param versao:
        :return:
        """
        for plataforma in self.get_plataformas():
            if plataforma.get_arquitetura() == arquitetura and versao == plataforma.get_versao():
                return plataforma

    def achar_ferramenta(self, nome, versao):
        """

        :param nome:
        :param versao:
        :return:
        """
        if self.get_ferramenta_por_nome(nome).get_versao() == versao:
            return self.get_ferramenta_por_nome(nome)
