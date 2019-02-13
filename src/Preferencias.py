#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Br.ino Qt preferencias

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

website: brino.cc
modificado por: Mateus Berardo
email: mateus.berardo@brino.cc
modificado por: Victor Rodrigues Pacheco
email: victor.pacheco@brino.cc
"""

import os

from MapaUtils import carregar, descarregar

preferencias = dict()


def init():
    """
    Carrega o arquivo de preferencias
    :return:
        None
    """
    global preferencias
    preferencias = carregar(os.path.join('builder', 'preferences.txt'))


def set(preferencia, valor):
    """
    Define a preferencia fornecida com o valor fornecido
    :param preferencia:
        Preferencia a ser salva
    :param valor:
        Valor da preferencia
    :return:
        None
    """
    preferencias[preferencia] = valor


def get(preferencia):
    """
    Busca a preferencia desejada
    :param preferencia:
        Preferencia a buscar
    :return:
        Valor da preferecia

    """
    return preferencias.get(preferencia)


def get_int(preferencia):
    """
    Retorna o valor da preferrencia como um inteiro
    :param preferencia:
        Preferencia a ser buscada
    :return:
        Valor inteiro da preferencia
    """
    return int(get(preferencia))


def get_float(preferencia):
    """
    TODO
    :param preferencia:
    :return:
    """
    return float(get(preferencia))


def get_mapa():
    """
    TODO
    :return:
    """
    return preferencias


def gravar_preferencias():
    """
        Salva as preferencias atualizadas no arquivo preferências

    :return:
        None
    """
    global preferencias
    descarregar(preferencias, os.path.join('builder', 'preferences.txt'))
    pass
